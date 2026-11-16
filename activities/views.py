import base64
import json
import uuid
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from .models import Workbook, Activity, ActivityProgress, Drawing


# Datos base del abecedario usando códigos vectoriales SVG (Twemoji CDN) y ruta local en static/
ALPHABET_DATA = [
    {'letter': 'A', 'slug': 'a', 'word': 'Avión', 'icon_code': '2708', 'color': '#FF6B6B'},
    {'letter': 'B', 'slug': 'b', 'word': 'Ballena', 'icon_code': '1f433', 'color': '#4ECDC4'},
    {'letter': 'C', 'slug': 'c', 'word': 'Casa', 'icon_code': '1f3e0', 'color': '#FFD166'},
    {'letter': 'D', 'slug': 'd', 'word': 'Dinosaurio', 'icon_code': '1f995', 'color': '#06D6A0'},
    {'letter': 'E', 'slug': 'e', 'word': 'Elefante', 'icon_code': '1f418', 'color': '#118AB2'},
    {'letter': 'F', 'slug': 'f', 'word': 'Flor', 'icon_code': '1f338', 'color': '#EF476F'},
    {'letter': 'G', 'slug': 'g', 'word': 'Gato', 'icon_code': '1f431', 'color': '#FF9F1C'},
    {'letter': 'H', 'slug': 'h', 'word': 'Helado', 'icon_code': '1f366', 'color': '#9B5DE5'},
    {'letter': 'I', 'slug': 'i', 'word': 'Isla', 'icon_code': '1f3dd', 'color': '#00BBF9'},
    {'letter': 'J', 'slug': 'j', 'word': 'Jirafa', 'icon_code': '1f992', 'color': '#F15BB5'},
    {'letter': 'K', 'slug': 'k', 'word': 'Koala', 'icon_code': '1f428', 'color': '#00F5D4'},
    {'letter': 'L', 'slug': 'l', 'word': 'León', 'icon_code': '1f981', 'color': '#FF6B6B'},
    {'letter': 'M', 'slug': 'm', 'word': 'Manzana', 'icon_code': '1f34e', 'color': '#4ECDC4'},
    {'letter': 'N', 'slug': 'n', 'word': 'Nube', 'icon_code': '2601', 'color': '#118AB2'},
    {'letter': 'Ñ', 'slug': 'enie', 'word': 'Ñandú', 'icon_code': '1f9a4', 'color': '#FFD166'},
    {'letter': 'O', 'slug': 'o', 'word': 'Oso', 'icon_code': '1f43b', 'color': '#06D6A0'},
    {'letter': 'P', 'slug': 'p', 'word': 'Perro', 'icon_code': '1f436', 'color': '#EF476F'},
    {'letter': 'Q', 'slug': 'q', 'word': 'Queso', 'icon_code': '1f9c0', 'color': '#FF9F1C'},
    {'letter': 'R', 'slug': 'r', 'word': 'Ratón', 'icon_code': '1f42d', 'color': '#9B5DE5'},
    {'letter': 'S', 'slug': 's', 'word': 'Sol', 'icon_code': '2600', 'color': '#00BBF9'},
    {'letter': 'T', 'slug': 't', 'word': 'Tortuga', 'icon_code': '1f422', 'color': '#06D6A0'},
    {'letter': 'U', 'slug': 'u', 'word': 'Uvas', 'icon_code': '1f347', 'color': '#9B5DE5'},
    {'letter': 'V', 'slug': 'v', 'word': 'Vaca', 'icon_code': '1f42e', 'color': '#FF6B6B'},
    {'letter': 'W', 'slug': 'w', 'word': 'Wafle', 'icon_code': '1f9c7', 'color': '#FF9F1C'},
    {'letter': 'X', 'slug': 'x', 'word': 'Xilófono', 'icon_code': '1f3bc', 'color': '#4ECDC4'},
    {'letter': 'Y', 'slug': 'y', 'word': 'Yoyo', 'icon_code': '1fa80', 'color': '#EF476F'},
    {'letter': 'Z', 'slug': 'z', 'word': 'Zanahoria', 'icon_code': '1f955', 'color': '#FF9F1C'},
]


@login_required
def home_view(request):
    completed_count = ActivityProgress.objects.filter(user=request.user, completed=True).count()
    drawings_count = Drawing.objects.filter(user=request.user).count()
    return render(request, 'activities/home.html', {
        'completed_count': completed_count,
        'drawings_count': drawings_count,
    })


@login_required
def alphabet_view(request):
    return render(request, 'activities/alphabet.html', {
        'alphabet': ALPHABET_DATA
    })


@login_required
def canvas_view(request):
    prompt_title = request.GET.get('prompt', 'Mi Dibujo Libre')
    user_drawings = Drawing.objects.filter(user=request.user)[:12]
    return render(request, 'activities/canvas.html', {
        'prompt_title': prompt_title,
        'drawings': user_drawings,
    })


@login_required
@require_POST
def save_drawing_api(request):
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        title = data.get('title', 'Mi Obra de Arte')[:100]

        if not image_data or ';base64,' not in image_data:
            return JsonResponse({'status': 'error', 'message': 'Imagen no válida.'}, status=400)

        format_part, imgstr = image_data.split(';base64,')
        ext = format_part.split('/')[-1]
        file_name = f"dibujo_{request.user.id}_{uuid.uuid4().hex[:8]}.{ext}"
        decoded_file = ContentFile(base64.b64decode(imgstr), name=file_name)

        # Guarda en PostgreSQL (Neon) y sube automáticamente el archivo a Cloudinary
        drawing = Drawing.objects.create(
            user=request.user,
            title=title or "Mi Obra de Arte",
            image=decoded_file
        )

        return JsonResponse({
            'status': 'ok',
            'message': '¡Dibujo guardado en tu galería!',
            'image_url': drawing.image.url,
            'title': drawing.title,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': "No se pudo guardar el dibujo."}, status=500)


@login_required
def workbook_list_view(request):
    workbooks = Workbook.objects.prefetch_related('activities').all()
    completed_ids = set(
        ActivityProgress.objects.filter(user=request.user, completed=True)
        .values_list('activity_id', flat=True)
    )
    return render(request, 'activities/workbook_list.html', {
        'workbooks': workbooks,
        'completed_ids': completed_ids,
    })


@login_required
def activity_detail_view(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    next_activity = Activity.objects.filter(
        workbook=activity.workbook,
        activity_number__gt=activity.activity_number
    ).first()

    is_completed = ActivityProgress.objects.filter(
        user=request.user, activity=activity, completed=True
    ).exists()

    return render(request, 'activities/activity_detail.html', {
        'activity': activity,
        'next_activity': next_activity,
        'is_completed': is_completed,
    })


@login_required
@require_POST
def check_activity_api(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    data = json.loads(request.body)
    user_answer = str(data.get('answer', '')).strip().lower()
    expected = str(activity.correct_answer).strip().lower()

    if activity.activity_type == 'drawing_prompt' or user_answer == expected:
        ActivityProgress.objects.update_or_create(
            user=request.user,
            activity=activity,
            defaults={'completed': True}
        )
        return JsonResponse({'correct': True, 'message': '¡Excelente trabajo! ⭐'})

    return JsonResponse({'correct': False, 'message': '¡Inténtalo otra vez! Tú puedes 💪'})