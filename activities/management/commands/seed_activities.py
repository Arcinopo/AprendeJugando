from django.core.management.base import BaseCommand
from activities.models import Workbook, Activity


class Command(BaseCommand):
    help = "Puebla la base de datos con actividades basadas en los cuadernillos pedagógicos PDF."

    def handle(self, *args, **kwargs):
        # 1. Cuadernillo de Lectoescritura
        wb_lecto, _ = Workbook.objects.get_or_create(
            title="Mi Cuaderno de Lectoescritura",
            defaults={
                'category': 'lectoescritura',
                'description': 'Vocales, sonido inicial, sílabas y primeras palabras.',
                'emoji_icon': '1f4d6',
                'color_theme': 'success',
                'order': 1,
            }
        )

        lecto_items = [
            (1, "Vocal Inicial A", "Observa la imagen y selecciona la vocal con la que empieza: Avión", "fill_vowel", "2708", "_ v i ó n", "A,E,I,O,U", "A"),
            (2, "Vocal Inicial E", "Completa con la vocal inicial de: Elefante", "fill_vowel", "1f418", "_ l e f a n t e", "A,E,I,O,U", "E"),
            (3, "Vocal Inicial I", "Completa con la vocal inicial de: Imán", "fill_vowel", "1f9f2", "_ m á n", "A,E,I,O,U", "I"),
            (4, "Vocal Inicial O", "Completa con la vocal inicial de: Oso", "fill_vowel", "1f43b", "_ s o", "A,E,I,O,U", "O"),
            (5, "Vocal Inicial U", "Completa con la vocal inicial de: Uvas", "fill_vowel", "1f347", "_ v a s", "A,E,I,O,U", "U"),
            (6, "Repaso de las 5 Vocales", "Completa la serie ordenada: A, E, __, O, U", "fill_vowel", "1f3b6", "A - E - [ ? ] - O - U", "A,E,I,O,U", "I"),
            (7, "Encuentra la Vocal Perdida", "Toca la vocal que falta en: Casa", "fill_vowel", "1f3e0", "C _ s a", "a,e,i,o,u", "a"),
            (8, "Sílaba Inicial M", "Completa con ma, me, mi, mo o mu: Mono", "fill_vowel", "1f412", "_ _ n o", "ma,me,mi,mo,mu", "mo"),
            (9, "Sílaba Inicial P", "Completa con pa, pe, pi, po o pu: Pato", "fill_vowel", "1f986", "_ _ t o", "pa,pe,pi,po,pu", "pa"),
            (10, "Une Palabra con Dibujo", "¿Cuál palabra corresponde a esta ilustración?", "match_pair", "1f319", "Elige el nombre correcto", "Sol,Luna,Estrella", "Luna"),
        ]

        for num, title, inst, atype, icon, prompt, opts, ans in lecto_items:
            Activity.objects.update_or_create(
                workbook=wb_lecto,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': opts,
                    'correct_answer': ans,
                }
            )

        # 2. Cuadernillo de Matemáticas Divertidas
        wb_math, _ = Workbook.objects.get_or_create(
            title="Matemáticas Divertidas",
            defaults={
                'category': 'matematica',
                'description': 'Conteo visual del 1 al 10, sumas ilustradas y patrones.',
                'emoji_icon': '1f522',
                'color_theme': 'primary',
                'order': 2,
            }
        )

        math_items = [
            (1, "Conteo de Manzanas", "Cuenta cuántas manzanas hay en la pantalla", "math_count", "1f34e,1f34e,1f34e", "¿Cuántas manzanas ves?", "1,2,3,4,5", "3"),
            (2, "Conteo de Estrellas", "Cuenta las estrellas brillantes", "math_count", "2b50,2b50,2b50,2b50", "¿Cuántas estrellas hay?", "2,3,4,5", "4"),
            (3, "Serie Numérica (1 al 5)", "Completa el número que falta en la serie", "math_count", "1f682", "1 - 2 - [ ? ] - 4 - 5", "2,3,4,6", "3"),
            (4, "Suma Ilustrada", "Cuenta todas las manzanas juntas", "math_count", "1f34e,2795,1f34e,1f34e", "1 + 2 = ?", "2,3,4,5", "3"),
            (5, "Patrón Círculo - Cuadrado", "Observa la secuencia y elige qué figura sigue", "match_pair", "1f534,1f7e6,1f534", "¿Qué figura sigue?", "Círculo,Cuadrado,Triángulo", "Cuadrado"),
        ]

        for num, title, inst, atype, icon, prompt, opts, ans in math_items:
            Activity.objects.update_or_create(
                workbook=wb_math,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': opts,
                    'correct_answer': ans,
                }
            )

        # 3. Cuadernillo de Creatividad (Retos para la Pizarra Digital)
        wb_creat, _ = Workbook.objects.get_or_create(
            title="Cuaderno de Creatividad",
            defaults={
                'category': 'creatividad',
                'description': 'Imaginación, dibujo libre y expresión artística en pizarra.',
                'emoji_icon': '1f3a8',
                'color_theme': 'warning',
                'order': 3,
            }
        )

        creat_items = [
            (1, "¿Qué hay dentro del círculo?", "Convierte un círculo en un animal u objeto divertido en la pizarra", "drawing_prompt", "2b55", "Abre la pizarra y dibuja tu creación", "", "COMPLETADO"),
            (2, "Diseña un sombrero loco", "Dibuja el sombrero más divertido del mundo", "drawing_prompt", "1f3a9", "Usa muchos colores en tu pizarra", "", "COMPLETADO"),
            (3, "Monstruo amigable", "Dibuja un monstruo simpático con 3 ojos y una gran sonrisa", "drawing_prompt", "1f47e", "¡Deja volar tu imaginación!", "", "COMPLETADO"),
            (4, "El gato astronauta", "Dibuja a un gatito explorando la luna y las estrellas", "drawing_prompt", "1f680", "Dibuja en tu pizarra mágica", "", "COMPLETADO"),
        ]

        for num, title, inst, atype, icon, prompt, opts, ans in creat_items:
            Activity.objects.update_or_create(
                workbook=wb_creat,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': opts,
                    'correct_answer': ans,
                }
            )

        # 4. Cuadernillo de Cuentos y Canciones
        wb_stories, _ = Workbook.objects.get_or_create(
            title="Mis Cuentos y Canciones",
            defaults={
                'category': 'cuentos',
                'description': 'Canciones infantiles tradicionales, rimas y cuentos clásicos.',
                'emoji_icon': '1f4da',
                'color_theme': 'danger',
                'order': 4,
            }
        )

        story_items = [
            (1, "Los Pollitos Dicen", "Canta: 'Los pollitos dicen pío, pío, pío, cuando tienen hambre...'", "match_pair", "1f424", "¿Qué dicen los pollitos?", "pío,mú,guau", "pío"),
            (2, "La Vaca Lola", "Canta: 'La vaca Lola tiene cabeza y tiene cola y hace...'", "match_pair", "1f42e", "¿Cómo hace la Vaca Lola?", "pío,mú,miau", "mú"),
            (3, "Los Tres Cerditos", "Había tres cerditos que construyeron casas de paja, madera y ladrillo.", "match_pair", "1f437", "¿Cuántos cerditos eran?", "2,3,4", "3"),
        ]

        for num, title, inst, atype, icon, prompt, opts, ans in story_items:
            Activity.objects.update_or_create(
                workbook=wb_stories,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': opts,
                    'correct_answer': ans,
                }
            )

        self.stdout.write(self.style.SUCCESS("¡Actividades de los cuadernillos cargadas exitosamente!"))
