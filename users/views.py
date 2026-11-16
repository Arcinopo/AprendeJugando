import json
import logging
import secrets
import urllib.request
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.conf import settings
from decouple import config
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import EmailVerificationCode
import urllib.error



logger = logging.getLogger(__name__)

def _send_otp_email(user):
    otp_obj, _ = EmailVerificationCode.objects.get_or_create(user=user)
    code = otp_obj.generate_new_code()

    _, sender_email = email.utils.parseaddr(settings.DEFAULT_FROM_EMAIL)
    sender_email = sender_email.strip()

    payload = {
        "sender": {
            "name": "AprendeJugando",
            "email": sender_email,
        },
        "to": [
            {
                "email": user.email.strip(),
            }
        ],
        "subject": "Tu código de verificación - AprendeJugando",
        "textContent": (
            f"¡Hola {user.first_name or user.username}!\n\n"
            f"Tu código mágico de 6 dígitos para activar tu cuenta en AprendeJugando es:\n\n"
            f"    {code}\n\n"
            f"Este código es válido por 15 minutos."
        ),
    }

    req = urllib.request.Request(
        url="https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status not in (200, 201, 202):
                raise RuntimeError(f"Brevo API respondió con estado {response.status}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"BREVO_API_ERROR ({e.code}) | sender={sender_email} | body={error_body}", flush=True)
        raise

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'users:login'


def register_view(request):
    if request.user.is_authenticated:
        return redirect('activities:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Limpia registros previos sin verificar con el mismo correo
            User.objects.filter(email=email, is_active=False).delete()

            user = form.save(commit=False)
            user.email = email
            user.is_active = False
            user.save()

            try:
                _send_otp_email(user)
                request.session['pending_user_id'] = user.id
                messages.info(request, f"Enviamos un código de 6 dígitos a {user.email}.")
                return redirect('users:verify_email')
            except Exception:
                logger.exception("Error al enviar correo OTP durante el registro para %s", user.email)
                user.delete()
                messages.error(
                    request,
                    "No se pudo enviar el correo de verificación en este momento. Intenta nuevamente."
                )
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def verify_email_view(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('users:register')

    user = User.objects.filter(id=user_id, is_active=False).first()
    if not user:
        request.session.pop('pending_user_id', None)
        return redirect('users:register')

    if request.method == 'POST':
        action = request.POST.get('action', 'verify')

        if action == 'resend':
            try:
                _send_otp_email(user)
                messages.success(request, f"¡Listo! Te enviamos un nuevo código a {user.email}.")
            except Exception:
                logger.exception("Error al reenviar correo OTP para %s", user.email)
                messages.error(request, "No se pudo reenviar el correo en este momento. Intenta más tarde.")
            return redirect('users:verify_email')

        entered_code = request.POST.get('code', '').strip()
        otp_obj = getattr(user, 'verification_code', None)

        if not otp_obj:
            messages.error(request, "No hay un código activo. Solicita uno nuevo.")
        elif otp_obj.is_expired():
            messages.warning(request, "El código venció (más de 15 min). Pulsa 'Reenviar código'.")
        elif secrets.compare_digest(otp_obj.code, entered_code):
            user.is_active = True
            user.save(update_fields=['is_active'])
            otp_obj.delete()
            request.session.pop('pending_user_id', None)

            login(request, user)
            messages.success(request, f"¡Cuenta activada! Bienvenido/a, {user.first_name or user.username}.")
            return redirect('activities:home')
        else:
            locked_out = otp_obj.register_failed_attempt()
            if locked_out:
                otp_obj.delete()
                messages.error(request, "Demasiados intentos fallidos. Solicita un nuevo código.")
            else:
                remaining = otp_obj.MAX_ATTEMPTS - otp_obj.attempts
                messages.error(request, f"Código incorrecto. Te quedan {remaining} intentos.")

    return render(request, 'users/verify_email.html', {'email': user.email})