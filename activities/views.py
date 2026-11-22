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
    completed_ids = set(
        ActivityProgress.objects.filter(user=request.user, completed=True)
        .values_list('activity_id', flat=True)
    )
    completed_count = len(completed_ids)
    total_activities = Activity.objects.count()
    overall_percentage = (
        int(round((completed_count / total_activities) * 100))
        if total_activities > 0
        else 0
    )
    drawings_count = Drawing.objects.filter(user=request.user).count()

    workbooks = Workbook.objects.prefetch_related('activities').all()
    completed_workbooks_count = 0
    for wb in workbooks:
        acts = list(wb.activities.all())
        if acts and all(act.id in completed_ids for act in acts):
            completed_workbooks_count += 1

    achievements = [
        {
            'title': 'Primer Paso',
            'description': 'Completa tu primera actividad.',
            'icon_code': '1f31f',
            'theme': 'warning',
            'unlocked': completed_count >= 1,
            'progress_label': f"{min(completed_count, 1)}/1 actividad",
        },
        {
            'title': 'Pequeño Artista',
            'description': 'Guarda tu primer dibujo en la pizarra.',
            'icon_code': '1f3a8',
            'theme': 'info',
            'unlocked': drawings_count >= 1,
            'progress_label': f"{min(drawings_count, 1)}/1 dibujo",
        },
        {
            'title': 'Explorador Curioso',
            'description': 'Completa 5 actividades de los cuadernillos.',
            'icon_code': '1f9ed',
            'theme': 'primary',
            'unlocked': completed_count >= 5,
            'progress_label': f"{min(completed_count, 5)}/5 actividades",
        },
        {
            'title': 'Galería Creativa',
            'description': 'Guarda 3 obras de arte en tu galería.',
            'icon_code': '1f5bc',
            'theme': 'danger',
            'unlocked': drawings_count >= 3,
            'progress_label': f"{min(drawings_count, 3)}/3 dibujos",
        },
        {
            'title': 'Maestro de Cuadernillo',
            'description': 'Termina al 100 % un cuadernillo completo.',
            'icon_code': '1f3c6',
            'theme': 'success',
            'unlocked': completed_workbooks_count >= 1,
            'progress_label': f"{min(completed_workbooks_count, 1)}/1 cuadernillo",
        },
        {
            'title': 'Súper Estudiante',
            'description': 'Alcanza 15 actividades completadas.',
            'icon_code': '1f680',
            'theme': 'primary',
            'unlocked': completed_count >= 15,
            'progress_label': f"{min(completed_count, 15)}/15 actividades",
        },
    ]
    unlocked_achievements_count = sum(1 for item in achievements if item['unlocked'])

    return render(request, 'activities/home.html', {
        'completed_count': completed_count,
        'total_activities': total_activities,
        'overall_percentage': overall_percentage,
        'drawings_count': drawings_count,
        'achievements': achievements,
        'unlocked_achievements_count': unlocked_achievements_count,
        'total_achievements_count': len(achievements),
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
        drawing_id = data.get('drawing_id')

        if not image_data or ';base64,' not in image_data:
            return JsonResponse({'status': 'error', 'message': 'Imagen no válida.'}, status=400)

        format_part, imgstr = image_data.split(';base64,')
        ext = format_part.split('/')[-1]
        file_name = f"dibujo_{request.user.id}_{uuid.uuid4().hex[:8]}.{ext}"
        decoded_file = ContentFile(base64.b64decode(imgstr), name=file_name)

        if drawing_id:
            try:
                drawing = Drawing.objects.get(id=drawing_id, user=request.user)
            except (Drawing.DoesNotExist, ValueError, TypeError):
                return JsonResponse(
                    {'status': 'error', 'message': 'El dibujo seleccionado no existe.'},
                    status=404
                )

            if drawing.image:
                drawing.image.delete(save=False)
            drawing.title = title or drawing.title or "Mi Obra de Arte"
            drawing.image = decoded_file
            drawing.save()
            message = '¡Dibujo actualizado en tu galería!'
        else:
            drawing = Drawing.objects.create(
                user=request.user,
                title=title or "Mi Obra de Arte",
                image=decoded_file
            )
            message = '¡Dibujo guardado en tu galería!'

        return JsonResponse({
            'status': 'ok',
            'message': message,
            'drawing_id': drawing.id,
            'image_url': drawing.image.url,
            'title': drawing.title,
        })
    except Exception:
        return JsonResponse({'status': 'error', 'message': "No se pudo guardar el dibujo."}, status=500)


@login_required
@require_POST
def delete_drawings_api(request):
    try:
        data = json.loads(request.body)
        raw_ids = data.get('drawing_ids', [])
        if not isinstance(raw_ids, list) or not raw_ids:
            return JsonResponse(
                {'status': 'error', 'message': 'Selecciona al menos un dibujo para eliminar.'},
                status=400
            )

        valid_ids = []
        for item in raw_ids:
            try:
                valid_ids.append(int(item))
            except (ValueError, TypeError):
                continue

        drawings_qs = Drawing.objects.filter(user=request.user, id__in=valid_ids)
        deleted_count = 0
        for drawing in drawings_qs:
            if drawing.image:
                drawing.image.delete(save=False)
            drawing.delete()
            deleted_count += 1

        return JsonResponse({
            'status': 'ok',
            'deleted_count': deleted_count,
            'message': f'Se eliminaron {deleted_count} dibujo(s) de tu galería.'
        })
    except Exception:
        return JsonResponse(
            {'status': 'error', 'message': 'No se pudieron eliminar los dibujos seleccionados.'},
            status=500
        )


@login_required
def workbook_list_view(request):
    workbooks = Workbook.objects.prefetch_related('activities').all()
    completed_ids = set(
        ActivityProgress.objects.filter(user=request.user, completed=True)
        .values_list('activity_id', flat=True)
    )

    for wb in workbooks:
        acts = list(wb.activities.all())
        wb.total_activities = len(acts)
        wb.completed_activities = sum(1 for act in acts if act.id in completed_ids)
        wb.progress_percent = (
            int(round((wb.completed_activities / wb.total_activities) * 100))
            if wb.total_activities > 0
            else 0
        )
        wb.is_completed = wb.total_activities > 0 and wb.completed_activities == wb.total_activities

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


def _mark_activity_completed(user, activity):
    ActivityProgress.objects.update_or_create(
        user=user,
        activity=activity,
        defaults={'completed': True}
    )


@login_required
@require_POST
def check_activity_api(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    data = json.loads(request.body)
    extra = activity.extra_data or {}

    # 1. Cazadores de errores
    if activity.activity_type == 'error_hunter':
        segments = extra.get('segments', [])
        if segments:
            corrections = data.get('corrections', {})
            all_fixed = True
            for idx, seg in enumerate(segments):
                if seg.get('is_error'):
                    expected_fix = str(seg.get('correction', '')).strip().lower()
                    given_fix = str(corrections.get(str(idx), '')).strip().lower()
                    if given_fix != expected_fix:
                        all_fixed = False
                        break
            if all_fixed:
                _mark_activity_completed(request.user, activity)
                return JsonResponse({
                    'correct': True,
                    'message': '¡Excelente trabajo de detective! Corregiste todos los errores.'
                })
            return JsonResponse({
                'correct': False,
                'message': 'Aún quedan errores por detectar o corregir. Revisa el texto con atención.'
            })

    # 2. Completar el cómic
    if activity.activity_type == 'comic_fill':
        panels = extra.get('panels', [])
        dialogues = data.get('dialogues', [])
        if len(dialogues) < len(panels):
            return JsonResponse({
                'correct': False,
                'message': 'Completa todos los globos de diálogo del cómic antes de terminar.'
            })
        for idx, panel in enumerate(panels):
            if not panel.get('readonly'):
                text_val = str(dialogues[idx]).strip()
                if len(text_val) < 2:
                    return JsonResponse({
                        'correct': False,
                        'message': f'Escribe un diálogo en la viñeta #{idx + 1} para continuar.'
                    })
        _mark_activity_completed(request.user, activity)
        return JsonResponse({
            'correct': True,
            'message': '¡Genial! Has creado una historieta muy creativa.'
        })

    # 3. Sopa de letras y Crucigrama temático
    if activity.activity_type == 'word_search':
        mode = extra.get('mode', 'soup')
        if mode == 'crossword':
            solution_grid = extra.get('solution_grid', [])
            grid_answers = data.get('grid_answers', {})
            for r_idx, row in enumerate(solution_grid):
                for c_idx, expected_char in enumerate(row):
                    if expected_char:
                        key = f"{r_idx},{c_idx}"
                        given_char = str(grid_answers.get(key, '')).strip().upper()
                        if given_char != str(expected_char).strip().upper():
                            return JsonResponse({
                                'correct': False,
                                'message': 'Revisa algunas letras del crucigrama. ¡Ya casi lo tienes!'
                            })
            _mark_activity_completed(request.user, activity)
            return JsonResponse({
                'correct': True,
                'message': '¡Crucigrama completado a la perfección!'
            })
        else:
            target_words = {
                str(item.get('word', '')).strip().upper()
                for item in extra.get('words', [])
                if item.get('word')
            }
            found_words = {str(w).strip().upper() for w in data.get('found_words', [])}
            if target_words and target_words.issubset(found_words):
                _mark_activity_completed(request.user, activity)
                return JsonResponse({
                    'correct': True,
                    'message': '¡Encontraste todas las palabras escondidas!'
                })
            return JsonResponse({
                'correct': False,
                'message': 'Todavía faltan palabras por encontrar en la sopa de letras.'
            })

    # 4. Laberinto numérico
    if activity.activity_type == 'math_maze':
        grid = extra.get('grid', [])
        steps = extra.get('steps', [])
        start = extra.get('start', [0, 0])
        submitted_path = data.get('path', [])

        if len(submitted_path) != len(steps) + 1:
            return JsonResponse({
                'correct': False,
                'message': 'Aún no has completado todo el recorrido del laberinto.'
            })

        if submitted_path[0] != start:
            return JsonResponse({
                'correct': False,
                'message': 'El recorrido debe comenzar en la casilla de salida.'
            })

        for idx, step in enumerate(steps):
            prev_r, prev_c = submitted_path[idx]
            curr_r, curr_c = submitted_path[idx + 1]
            if abs(prev_r - curr_r) + abs(prev_c - curr_c) != 1:
                return JsonResponse({
                    'correct': False,
                    'message': 'Solo puedes avanzar a casillas vecinas (arriba, abajo, izquierda o derecha).'
                })
            if not (0 <= curr_r < len(grid) and 0 <= curr_c < len(grid[0])):
                return JsonResponse({
                    'correct': False,
                    'message': 'Movimiento fuera del tablero.'
                })
            if grid[curr_r][curr_c] != step.get('answer'):
                return JsonResponse({
                    'correct': False,
                    'message': f'El resultado de {step.get("expression")} no coincide con esa casilla.'
                })

        _mark_activity_completed(request.user, activity)
        return JsonResponse({
            'correct': True,
            'message': '¡Lograste salir del laberinto resolviendo todas las operaciones!'
        })

    # 5. Sudoku visual 4x4
    if activity.activity_type == 'visual_sudoku':
        solution = extra.get('solution', [])
        grid_answers = data.get('grid_answers', {})
        if not solution:
            return JsonResponse({'correct': False, 'message': 'Tablero no configurado.'}, status=400)

        for r_idx, row in enumerate(solution):
            for c_idx, expected_key in enumerate(row):
                key = f"{r_idx},{c_idx}"
                given_key = str(grid_answers.get(key, '')).strip()
                if given_key != str(expected_key).strip():
                    return JsonResponse({
                        'correct': False,
                        'message': 'Revisa el tablero: ninguna figura debe repetirse en la misma fila, columna o bloque 2x2.'
                    })

        _mark_activity_completed(request.user, activity)
        return JsonResponse({
            'correct': True,
            'message': '¡Sudoku visual completado sin ningún error!'
        })

    # 6. Encuentra las diferencias
    if activity.activity_type == 'spot_differences':
        differences = extra.get('differences', [])
        expected_ids = {str(d.get('id')) for d in differences if d.get('id')}
        found_ids = {str(item) for item in data.get('found_ids', [])}

        if expected_ids and expected_ids.issubset(found_ids):
            _mark_activity_completed(request.user, activity)
            return JsonResponse({
                'correct': True,
                'message': f'¡Vista de águila! Encontraste las {len(expected_ids)} diferencias.'
            })

        missing = len(expected_ids - found_ids)
        return JsonResponse({
            'correct': False,
            'message': f'Te faltan {missing} diferencia(s) por encontrar en la imagen de la derecha.'
        })

    # 7. Experimento casero paso a paso y ficha de observación (Ciencias)
    if activity.activity_type == 'science_experiment':
        selected_hypothesis = str(data.get('hypothesis', '')).strip().lower()
        observation_text = str(data.get('observation', '')).strip()
        expected_hypothesis = str(extra.get('correct_hypothesis', '')).strip().lower()

        if not selected_hypothesis:
            return JsonResponse({
                'correct': False,
                'message': 'Selecciona una hipótesis antes de registrar el resultado del experimento.'
            })

        if len(observation_text) < 4:
            return JsonResponse({
                'correct': False,
                'message': 'Escribe lo que observaste al realizar el experimento en tu ficha.'
            })

        if selected_hypothesis != expected_hypothesis:
            return JsonResponse({
                'correct': False,
                'message': 'La hipótesis elegida no coincide con lo que ocurre en el experimento. ¡Vuelve a intentarlo!'
            })

        _mark_activity_completed(request.user, activity)
        return JsonResponse({
            'correct': True,
            'message': '¡Excelente trabajo científico! Tu ficha de observación quedó registrada.',
            'explanation': extra.get('explanation', '')
        })

    # 8. Clasificación por categorías (Ciencias)
    if activity.activity_type == 'category_sort':
        elements = extra.get('elements', [])
        assignments = data.get('assignments', {})

        if len(assignments) < len(elements):
            return JsonResponse({
                'correct': False,
                'message': 'Aún quedan elementos sin clasificar en las tablas.'
            })

        for el in elements:
            el_id = str(el.get('id'))
            expected_cat = str(el.get('category_id'))
            given_cat = str(assignments.get(el_id, ''))
            if given_cat != expected_cat:
                return JsonResponse({
                    'correct': False,
                    'message': f'Revisa dónde ubicaste "{el.get("name")}". ¡Inténtalo de nuevo!'
                })

        _mark_activity_completed(request.user, activity)
        return JsonResponse({
            'correct': True,
            'message': '¡Clasificación perfecta! Ubicaste todos los elementos en su categoría.'
        })

    # 9. Problema matemático contextualizado y tipos clásicos
    user_answer = str(data.get('answer', '')).strip().lower()
    expected = str(activity.correct_answer).strip().lower()

    if activity.activity_type == 'drawing_prompt' or user_answer == expected:
        _mark_activity_completed(request.user, activity)
        return JsonResponse({'correct': True, 'message': '¡Excelente trabajo!'})

    return JsonResponse({'correct': False, 'message': '¡Inténtalo otra vez! Tú puedes.'})