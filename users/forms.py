from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre del niño/a",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg rounded-4',
            'placeholder': 'Ej. Sofía o Mateo'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico (Padre/Madre)",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg rounded-4',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario mágico"
        self.fields['username'].help_text = "Letras o números sin espacios."
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg rounded-4'})

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Este correo electrónico ya tiene una cuenta activa.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario mágico"
        self.fields['password'].label = "Contraseña secreta"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg rounded-4'})