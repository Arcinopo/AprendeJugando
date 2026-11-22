from django.core.management.base import BaseCommand
from activities.models import Workbook, Activity


class Command(BaseCommand):
    help = "Puebla la base de datos con actividades para Inicial y Primaria."

    def handle(self, *args, **kwargs):
        # 1. Cuadernillo de Lectoescritura (Inicial)
        wb_lecto, _ = Workbook.objects.get_or_create(
            title="Mi Cuaderno de Lectoescritura",
            defaults={
                'category': 'lectoescritura',
                'grade_level': 'inicial',
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

        # 2. Cuadernillo de Matemáticas Divertidas (Inicial)
        wb_math, _ = Workbook.objects.get_or_create(
            title="Matemáticas Divertidas",
            defaults={
                'category': 'matematica',
                'grade_level': 'inicial',
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

        # 3. Cuadernillo de Creatividad (Todos los niveles)
        wb_creat, _ = Workbook.objects.get_or_create(
            title="Cuaderno de Creatividad",
            defaults={
                'category': 'creatividad',
                'grade_level': 'todos',
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

        # 4. Cuadernillo de Cuentos y Canciones (Inicial)
        wb_stories, _ = Workbook.objects.get_or_create(
            title="Mis Cuentos y Canciones",
            defaults={
                'category': 'cuentos',
                'grade_level': 'inicial',
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

        # 5. Cuadernillo de Comprensión Lectora y Lenguaje (Primaria)
        wb_primaria_lang, _ = Workbook.objects.get_or_create(
            title="Comprensión Lectora y Lenguaje",
            defaults={
                'category': 'comprension',
                'grade_level': 'primaria',
                'description': 'Cazadores de errores, cómics creativos, sopas de letras y crucigramas.',
                'emoji_icon': '1f50d',
                'color_theme': 'info',
                'order': 5,
            }
        )

        primaria_lang_items = [
            (
                1,
                "Cazadores de Errores: El Perro Volador",
                "Lee con atención, toca las palabras repetidas o absurdas y corrígelas.",
                "error_hunter",
                "1f436",
                "",
                {
                    "segments": [
                        {"text": "Ayer por la tarde, ", "is_error": False},
                        {
                            "text": "el el",
                            "is_error": True,
                            "correction": "el",
                            "options": ["el", "los", "unas"],
                            "reason": "Hay una palabra repetida."
                        },
                        {"text": " perro de Sofía salió al jardín y ", "is_error": False},
                        {
                            "text": "voló hacia su nido",
                            "is_error": True,
                            "correction": "corrió hacia su caseta",
                            "options": ["voló hacia su nido", "corrió hacia su caseta", "nadó en las nubes"],
                            "reason": "Dato absurdo: los perros no vuelan ni duermen en nidos."
                        },
                        {"text": " para descansar.", "is_error": False},
                    ]
                }
            ),
            (
                2,
                "Cazadores de Errores: El Pirata y el Sombrero",
                "Encuentra las 2 palabras incorrectas en el texto y selecciona la corrección adecuada.",
                "error_hunter",
                "1f3f4-200d-2620-fe0f",
                "",
                {
                    "segments": [
                        {"text": "Había una vez un pirata que navegaba por los mares en su barco junto a un loro parlanchín. Un día soleado, decidió comprar un ", "is_error": False},
                        {
                            "text": "zombrerero",
                            "is_error": True,
                            "correction": "sombrero",
                            "options": ["zombrerero", "sombrero", "sombrerera"],
                            "reason": "La palabra sombrero se escribe con 's' y no con 'z'."
                        },
                        {"text": " de paja para protegerse del sol. Más tarde, saltó al agua para nadar cerca de un ", "is_error": False},
                        {
                            "text": "zapato",
                            "is_error": True,
                            "correction": "barco",
                            "options": ["zapato", "barco", "avión"],
                            "reason": "Los piratas navegan por el océano en un barco, no en un zapato."
                        },
                        {"text": " de madera que flotaba en la bahía.", "is_error": False},
                    ]
                }
            ),
            (
                3,
                "Cazadores de Errores: El Bombero Dulcero",
                "Lee el texto y detecta los 2 errores ortográficos antes de la 'p' y la 'b'.",
                "error_hunter",
                "1f692",
                "",
                {
                    "segments": [
                        {"text": "El simpático ", "is_error": False},
                        {
                            "text": "bonbero",
                            "is_error": True,
                            "correction": "bombero",
                            "options": ["bonbero", "bombero", "bambero"],
                            "reason": "Siempre se escribe 'm' antes de la letra 'b'."
                        },
                        {"text": " acudió al campamento de verano a apagar una pequeña fogata. Al terminar, la cocinera le regaló un sabroso ", "is_error": False},
                        {
                            "text": "conbón",
                            "is_error": True,
                            "correction": "bombón",
                            "options": ["conbón", "bombón", "bonbón"],
                            "reason": "Se escribe 'm' antes de 'b' y de 'p'."
                        },
                        {"text": " de chocolate con avellanas.", "is_error": False},
                    ]
                }
            ),
            (
                4,
                "Completa el Cómic: Encuentro Espacial",
                "Inventa los diálogos entre Luna y el pequeño visitante espacial.",
                "comic_fill",
                "1f680",
                "Observa las viñetas y escribe qué dicen o piensan los personajes.",
                {
                    "panels": [
                        {
                            "character_name": "Astronauta Luna",
                            "character_icon": "1f469-200d-1f680",
                            "scene_bg": "#E0F2FE",
                            "narration": "Al aterrizar en un planeta desconocido...",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué dice Luna al bajar de su cohete?",
                        },
                        {
                            "character_name": "Amiguito Zorg",
                            "character_icon": "1f47d",
                            "scene_bg": "#DCFCE7",
                            "narration": "De pronto aparece un habitante muy simpático.",
                            "bubble_type": "speech",
                            "placeholder": "¿Cómo responde el extraterrestre?",
                        },
                        {
                            "character_name": "Astronauta Luna",
                            "character_icon": "1f469-200d-1f680",
                            "scene_bg": "#FEF3C7",
                            "narration": "Juntos deciden explorar el lugar.",
                            "bubble_type": "thought",
                            "placeholder": "¿Qué piensa Luna sobre su nuevo amigo?",
                        },
                    ]
                }
            ),
            (
                5,
                "Completa el Cómic: Plantando una Semilla",
                "Escribe los diálogos de los personajes para completar la historieta sobre cómo crece una planta.",
                "comic_fill",
                "1f331",
                "Un niño le enseña a su amiga el proceso de germinación de una semilla en una maceta.",
                {
                    "panels": [
                        {
                            "character_name": "Mateo",
                            "character_icon": "1f466",
                            "scene_bg": "#ECFDF5",
                            "narration": "En la primera viñeta, Mateo coloca la semilla en la tierra de la maceta.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué le dice a su amiga mientras pone la semilla?",
                        },
                        {
                            "character_name": "Mateo",
                            "character_icon": "1f466",
                            "scene_bg": "#E0F2FE",
                            "narration": "En la segunda viñeta, la riegan suavemente con una regadera.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué le explica sobre el agua y la luz del sol?",
                        },
                        {
                            "character_name": "Camila",
                            "character_icon": "1f467",
                            "scene_bg": "#FEF9C3",
                            "narration": "Mateo le adelanta que brotará una flor y Camila reacciona sorprendida.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué exclama Camila al saber de antemano el final?",
                        },
                    ]
                }
            ),
            (
                6,
                "Completa el Cómic: El Vendedor de Globos",
                "Completa los globos de diálogo de esta aventura en el parque.",
                "comic_fill",
                "1f388",
                "Un vendedor de globos se encuentra con un personaje travieso en el parque.",
                {
                    "panels": [
                        {
                            "character_name": "Vendedor de Globos",
                            "character_icon": "1f9d1",
                            "scene_bg": "#EFF6FF",
                            "narration": "El vendedor llega al parque promocionando sus vistosos globos de colores.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué grita el vendedor para ofrecer sus globos?",
                        },
                        {
                            "character_name": "Personaje Travieso",
                            "character_icon": "1f9d9",
                            "scene_bg": "#FEE2E2",
                            "narration": "Aparece un personaje travieso con intención de reventarlos.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué dice al ver todos los globos?",
                        },
                        {
                            "character_name": "Vendedor de Globos",
                            "character_icon": "1f9d1",
                            "scene_bg": "#DCFCE7",
                            "narration": "El vendedor le regala un globo para volar alto y hacerse amigos.",
                            "bubble_type": "speech",
                            "placeholder": "¿Qué le propone para evitar que pinche los globos?",
                        },
                    ]
                }
            ),
            (
                7,
                "Sopa de Letras: Animales del Entorno",
                "Encuentra las 4 palabras de animales escondidas en la cuadrícula.",
                "word_search",
                "1f43e",
                "",
                {
                    "mode": "soup",
                    "theme_name": "Animales del Entorno",
                    "grid": [
                        ["G", "A", "T", "O", "X", "Y", "Z", "W"],
                        ["L", "O", "R", "O", "A", "B", "C", "D"],
                        ["V", "A", "C", "A", "E", "F", "G", "H"],
                        ["R", "A", "N", "A", "I", "J", "K", "L"],
                        ["M", "N", "O", "P", "Q", "R", "S", "T"],
                        ["U", "V", "W", "X", "Y", "Z", "A", "B"],
                        ["C", "D", "E", "F", "G", "H", "I", "J"],
                        ["K", "L", "M", "N", "O", "P", "Q", "R"],
                    ],
                    "words": [
                        {"word": "GATO", "icon": "1f431", "clue": "Mamífero doméstico que maúlla."},
                        {"word": "LORO", "icon": "1f99c", "clue": "Ave parlanchina de plumas vistosas."},
                        {"word": "VACA", "icon": "1f42e", "clue": "Mamífero de granja que da leche."},
                        {"word": "RANA", "icon": "1f438", "clue": "Anfibio que canta cerca del agua."},
                    ]
                }
            ),
            (
                8,
                "Sopa de Letras: El Mundo Vegetal",
                "Localiza 4 términos relacionados con las plantas en el panel 8x8.",
                "word_search",
                "1f33f",
                "",
                {
                    "mode": "soup",
                    "theme_name": "Partes y Tipos de Plantas",
                    "grid": [
                        ["F", "L", "O", "R", "X", "Y", "Z", "W"],
                        ["H", "O", "J", "A", "A", "B", "C", "D"],
                        ["R", "A", "M", "A", "E", "F", "G", "H"],
                        ["R", "O", "B", "L", "E", "I", "J", "K"],
                        ["L", "M", "N", "O", "P", "Q", "R", "S"],
                        ["T", "U", "V", "W", "X", "Y", "Z", "A"],
                        ["B", "C", "D", "E", "F", "G", "H", "I"],
                        ["J", "K", "L", "M", "N", "O", "P", "Q"],
                    ],
                    "words": [
                        {"word": "FLOR", "icon": "1f33b", "clue": "Estructura vistosa de las plantas de colores."},
                        {"word": "HOJA", "icon": "1f343", "clue": "Órgano vegetal que realiza la fotosíntesis."},
                        {"word": "RAMA", "icon": "1f33f", "clue": "Parte del árbol que sostiene las hojas."},
                        {"word": "ROBLE", "icon": "1f333", "clue": "Ejemplo de árbol grande de tronco leñoso."},
                    ]
                }
            ),
            (
                9,
                "Crucigrama Temático: Profesiones",
                "Lee las pistas horizontales y verticales y escribe cada profesión.",
                "word_search",
                "1f9d1-200d-1f3eb",
                "",
                {
                    "mode": "crossword",
                    "theme_name": "Profesiones y Oficios",
                    "solution_grid": [
                        ["M", "A", "E", "S", "T", "R", "A"],
                        ["E", "",  "",  "",  "",  "",  "C"],
                        ["D", "",  "",  "",  "",  "",  "T"],
                        ["I", "",  "",  "",  "",  "",  "O"],
                        ["C", "H", "E", "F", "",  "",  "R"],
                        ["O", "",  "",  "",  "",  "",  ""],
                    ],
                    "cell_numbers": {
                        "0,0": 1,
                        "0,6": 2,
                        "4,0": 3,
                    },
                    "clues": {
                        "across": [
                            {"num": 1, "clue": "Enseña a los niños en la escuela (7 letras)"},
                            {"num": 3, "clue": "Prepara deliciosas comidas en la cocina (4 letras)"},
                        ],
                        "down": [
                            {"num": 1, "clue": "Cura a las personas cuando están enfermas (6 letras)"},
                            {"num": 2, "clue": "Interpreta personajes en el teatro o cine (5 letras)"},
                        ]
                    }
                }
            ),
        ]

        for num, title, inst, atype, icon, prompt, extra in primaria_lang_items:
            Activity.objects.update_or_create(
                workbook=wb_primaria_lang,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': '',
                    'correct_answer': 'COMPLETADO',
                    'extra_data': extra,
                }
            )

        # 6. Cuadernillo de Matemáticas para Primaria
        wb_primaria_math, _ = Workbook.objects.get_or_create(
            title="Matemáticas de Primaria",
            defaults={
                'category': 'matematica',
                'grade_level': 'primaria',
                'description': 'Laberintos numéricos, sudokus visuales, retos visuales y problemas reales.',
                'emoji_icon': '1f9ee',
                'color_theme': 'primary',
                'order': 6,
            }
        )

        primaria_math_items = [
            (
                1,
                "Laberinto de las Tablas de Multiplicar",
                "Avanza desde Inicio hasta la Meta eligiendo solo las casillas con el resultado correcto.",
                "math_maze",
                "1f9ed",
                "",
                "",
                "COMPLETADO",
                {
                    "start": [0, 0],
                    "goal": [3, 3],
                    "grid": [
                        [0,  12, 14, 25],
                        [9,  24, 21, 30],
                        [15, 20, 35, 32],
                        [18, 27, 40, 48],
                    ],
                    "steps": [
                        {"expression": "3 x 4", "answer": 12},
                        {"expression": "6 x 4", "answer": 24},
                        {"expression": "7 x 3", "answer": 21},
                        {"expression": "5 x 7", "answer": 35},
                        {"expression": "8 x 5", "answer": 40},
                        {"expression": "6 x 8", "answer": 48},
                    ]
                }
            ),
            (
                2,
                "Laberinto Matemático: Sumando de 2 en 2",
                "Avanza desde la casilla inicial hasta la meta siguiendo las casillas que continúan la suma.",
                "math_maze",
                "1f3af",
                "",
                "",
                "COMPLETADO",
                {
                    "start": [0, 0],
                    "goal": [3, 3],
                    "grid": [
                        [0,  2,  5,  9],
                        [3,  4,  6,  11],
                        [7,  13, 8,  15],
                        [14, 16, 10, 12],
                    ],
                    "steps": [
                        {"expression": "0 + 2", "answer": 2},
                        {"expression": "2 + 2", "answer": 4},
                        {"expression": "4 + 2", "answer": 6},
                        {"expression": "6 + 2", "answer": 8},
                        {"expression": "8 + 2", "answer": 10},
                        {"expression": "10 + 2", "answer": 12},
                    ]
                }
            ),
            (
                3,
                "Laberinto Matemático: La Tabla del 3",
                "Resuelve cada multiplicación para abrirte paso por el laberinto hasta la meta.",
                "math_maze",
                "1f680",
                "",
                "",
                "COMPLETADO",
                {
                    "start": [0, 0],
                    "goal": [3, 3],
                    "grid": [
                        [0, 4,  8,  11],
                        [3, 7,  10, 14],
                        [6, 9,  12, 16],
                        [5, 13, 15, 18],
                    ],
                    "steps": [
                        {"expression": "1 x 3", "answer": 3},
                        {"expression": "2 x 3", "answer": 6},
                        {"expression": "3 x 3", "answer": 9},
                        {"expression": "4 x 3", "answer": 12},
                        {"expression": "5 x 3", "answer": 15},
                        {"expression": "6 x 3", "answer": 18},
                    ]
                }
            ),
            (
                4,
                "Sudoku Visual: Frutas Saludables",
                "Completa el tablero 4x4 colocando las 4 frutas sin repetir ninguna en la misma fila, columna o bloque 2x2.",
                "visual_sudoku",
                "1f34e",
                "",
                "",
                "COMPLETADO",
                {
                    "items": {
                        "k1": {"label": "Manzana", "icon_code": "1f34e"},
                        "k2": {"label": "Plátano", "icon_code": "1f34c"},
                        "k3": {"label": "Naranja", "icon_code": "1f34a"},
                        "k4": {"label": "Uva", "icon_code": "1f347"},
                    },
                    "initial": [
                        ["k1", "k2", "",   "k4"],
                        ["",   "k4", "k1", ""],
                        ["",   "k1", "k4", ""],
                        ["k4", "",   "k2", "k1"],
                    ],
                    "solution": [
                        ["k1", "k2", "k3", "k4"],
                        ["k3", "k4", "k1", "k2"],
                        ["k2", "k1", "k4", "k3"],
                        ["k4", "k3", "k2", "k1"],
                    ]
                }
            ),
            (
                5,
                "Sudoku Visual: Figuras Geométricas",
                "Rellena el tablero 4x4 para que cada símbolo aparezca una vez por fila, columna y bloque 2x2.",
                "visual_sudoku",
                "1f53a",
                "",
                "",
                "COMPLETADO",
                {
                    "items": {
                        "k1": {"label": "Círculo", "icon_code": "1f534"},
                        "k2": {"label": "Cuadrado", "icon_code": "1f7e6"},
                        "k3": {"label": "Triángulo", "icon_code": "1f53a"},
                        "k4": {"label": "Estrella", "icon_code": "2b50"},
                    },
                    "initial": [
                        ["k4", "",   "",   "k1"],
                        ["",   "k1", "k4", ""],
                        ["",   "k4", "k1", ""],
                        ["k1", "",   "",   "k4"],
                    ],
                    "solution": [
                        ["k4", "k3", "k2", "k1"],
                        ["k2", "k1", "k4", "k3"],
                        ["k3", "k4", "k1", "k2"],
                        ["k1", "k2", "k3", "k4"],
                    ]
                }
            ),
            (
                6,
                "Encuentra las 6 Diferencias: Día en el Parque",
                "Observa con mucha atención y toca las 6 diferencias en la imagen de la derecha.",
                "spot_differences",
                "1f50e",
                "",
                "",
                "COMPLETADO",
                {
                    "base_elements": [
                        {"id": "sun", "x": 16, "y": 18, "size": 48, "icon_code": "2600", "label": "Sol"},
                        {"id": "cloud", "x": 62, "y": 20, "size": 46, "icon_code": "2601", "label": "Nube"},
                        {"id": "bird", "x": 82, "y": 28, "size": 34, "icon_code": "1f426", "label": "Pajarito"},
                        {"id": "tree", "x": 24, "y": 58, "size": 68, "icon_code": "1f333", "label": "Árbol"},
                        {"id": "house", "x": 74, "y": 60, "size": 64, "icon_code": "1f3e1", "label": "Casa"},
                        {"id": "dog", "x": 48, "y": 78, "size": 42, "icon_code": "1f436", "label": "Perrito"},
                        {"id": "flower", "x": 15, "y": 84, "size": 34, "icon_code": "1f33b", "label": "Girasol"},
                    ],
                    "differences": [
                        {
                            "id": "diff_sun",
                            "target_id": "sun",
                            "x": 16,
                            "y": 18,
                            "mode": "replace",
                            "override": {"icon_code": "1f324"},
                            "label": "El sol tiene una nube"
                        },
                        {
                            "id": "diff_bird",
                            "target_id": "bird",
                            "x": 82,
                            "y": 28,
                            "mode": "hide",
                            "label": "Falta el pajarito"
                        },
                        {
                            "id": "diff_tree",
                            "target_id": "tree",
                            "x": 24,
                            "y": 58,
                            "mode": "replace",
                            "override": {"icon_code": "1f334"},
                            "label": "El árbol cambió a palmera"
                        },
                        {
                            "id": "diff_dog",
                            "target_id": "dog",
                            "x": 48,
                            "y": 78,
                            "mode": "replace",
                            "override": {"flip": True},
                            "label": "El perrito mira al otro lado"
                        },
                        {
                            "id": "diff_flower",
                            "target_id": "flower",
                            "x": 15,
                            "y": 84,
                            "mode": "replace",
                            "override": {"icon_code": "1f337"},
                            "label": "La flor cambió a tulipán"
                        },
                        {
                            "id": "diff_butterfly",
                            "x": 54,
                            "y": 46,
                            "mode": "add",
                            "element": {"x": 54, "y": 46, "size": 34, "icon_code": "1f98b", "label": "Mariposa"},
                            "label": "Apareció una mariposa"
                        },
                    ]
                }
            ),
            (
                7,
                "De Compras en la Tiendita",
                "Calcula cuánto dinero te devuelven después de pagar tus compras.",
                "math_problem",
                "1f6d2",
                "",
                "$15,$20,$25,$30",
                "$20",
                {
                    "context_title": "Tienda Escolar",
                    "story": "Camila lleva un billete de $50 para comprar útiles escolares. Elige 1 cuaderno, 1 caja de lápices y 1 regla.",
                    "items": [
                        {"name": "Cuaderno", "value": "$18", "icon_code": "1f4d3"},
                        {"name": "Lápices", "value": "$7", "icon_code": "270f"},
                        {"name": "Regla", "value": "$5", "icon_code": "1f4cf"},
                    ],
                    "question": "Si paga con $50, ¿cuánto vuelto debe recibir Camila?"
                }
            ),
            (
                8,
                "Receta de Galletas para Compartir",
                "Calcula los ingredientes necesarios para preparar el doble de la receta.",
                "math_problem",
                "1f36a",
                "",
                "400 gramos,500 gramos,600 gramos,750 gramos",
                "500 gramos",
                {
                    "context_title": "Taller de Cocina",
                    "story": "La receta original rinde para 10 galletas y usa estos ingredientes. Hoy vendrán 20 amigos a merendar, así que necesitas preparar el doble.",
                    "items": [
                        {"name": "Harina (10 galletas)", "value": "250 gramos", "icon_code": "1f33e"},
                        {"name": "Huevos (10 galletas)", "value": "2 unidades", "icon_code": "1f95a"},
                        {"name": "Chispas (10 galletas)", "value": "100 gramos", "icon_code": "1f36b"},
                    ],
                    "question": "¿Cuántos gramos de harina necesitas en total para hacer 20 galletas?"
                }
            ),
            (
                9,
                "Compras en la Pizzería",
                "Calcula el costo total y el vuelto a devolver en la compra.",
                "math_problem",
                "1f355",
                "",
                "3,38 €,4,38 €,5,38 €,4,65 €",
                "4,38 €",
                {
                    "context_title": "Supermercado Escolar",
                    "story": "Lucía va al supermercado a comprar 3 pizzas individuales a 1,55 € cada una y 1 botella de zumo por 0,97 €. Paga en caja con un billete de 10 €.",
                    "items": [
                        {"name": "3 pizzas (1,55 € c/u)", "value": "4,65 €", "icon_code": "1f355"},
                        {"name": "1 botella de zumo", "value": "0,97 €", "icon_code": "1f9c3"},
                    ],
                    "question": "¿Cuánto dinero le deben devolver de cambio a Lucía tras pagar con el billete de 10 €?"
                }
            ),
            (
                10,
                "Ingredientes para la Tarta",
                "Resuelve la situación problemática planteada en la cocina.",
                "math_problem",
                "1f967",
                "",
                "0,50 €,0,80 €,1,20 €,1,80 €",
                "0,80 €",
                {
                    "context_title": "Receta de Tarta",
                    "story": "Carlos compra 2 kilos de manzanas a 1,50 € el kilo y 1 paquete de harina a 1,20 € para hornear una tarta. Si paga toda la compra con un billete de 5 €...",
                    "items": [
                        {"name": "2 kg de manzanas (1,50 €/kg)", "value": "3,00 €", "icon_code": "1f34e"},
                        {"name": "1 paquete de harina", "value": "1,20 €", "icon_code": "1f33e"},
                    ],
                    "question": "¿Cuánto cambio le devuelven al pagar la compra con el billete de 5 €?"
                }
            ),
        ]

        for num, title, inst, atype, icon, prompt, opts, ans, extra in primaria_math_items:
            Activity.objects.update_or_create(
                workbook=wb_primaria_math,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': prompt,
                    'options': opts,
                    'correct_answer': ans,
                    'extra_data': extra,
                }
            )

        # 7. Cuadernillo de Ciencias y Experimentos (Primaria)
        wb_primaria_science, _ = Workbook.objects.get_or_create(
            title="Ciencias y Experimentos",
            defaults={
                'category': 'ciencias',
                'grade_level': 'primaria',
                'description': 'Experimentos caseros paso a paso con ficha de observación y clasificación científica.',
                'emoji_icon': '1f52c',
                'color_theme': 'success',
                'order': 7,
            }
        )

        primaria_science_items = [
            (
                1,
                "El Huevo Flotante y la Densidad",
                "Realiza el experimento casero y comprueba tu hipótesis sobre la flotabilidad del agua salada.",
                "science_experiment",
                "1f95a",
                {
                    "materials": [
                        "2 vasos transparentes",
                        "Agua del grifo",
                        "6 cucharadas soperas de sal",
                        "2 huevos crudos frescos",
                        "1 cuchara"
                    ],
                    "steps": [
                        "Llena los dos vasos transparentes con agua dulce hasta la mitad.",
                        "Agrega las 6 cucharadas de sal al Vaso B y remueve bien hasta disolverla por completo.",
                        "Introduce un huevo en el Vaso A (agua sola) y otro en el Vaso B (agua salada) y compara sus posiciones."
                    ],
                    "hypothesis_question": "¿Qué le ocurrirá al huevo colocado en el Vaso B con agua salada?",
                    "hypothesis_options": [
                        "El huevo se hundirá hasta tocar el fondo.",
                        "El huevo flotará en la superficie.",
                        "El huevo se romperá al entrar al agua."
                    ],
                    "correct_hypothesis": "El huevo flotará en la superficie.",
                    "explanation": "Al disolver sal en el agua, aumenta su densidad. El agua salada ejerce un empuje hacia arriba superior al peso del huevo, haciendo que flote."
                }
            ),
            (
                2,
                "Volcán de Vinagre y Bicarbonato",
                "Observa una reacción química efervescente segura utilizando elementos cotidianos.",
                "science_experiment",
                "1f30b",
                {
                    "materials": [
                        "1 vaso pequeño o botella de plástico",
                        "2 cucharadas de bicarbonato de sodio",
                        "Medio vaso de vinagre",
                        "Unas gotas de colorante alimentario (opcional)"
                    ],
                    "steps": [
                        "Deposita las 2 cucharadas de bicarbonato de sodio en el fondo del vaso o botella.",
                        "Añade las gotas de colorante si deseas que la mezcla tenga color vistoso.",
                        "Vierte con cuidado el vinagre en el recipiente y observa la reacción inmediata."
                    ],
                    "hypothesis_question": "¿Qué fenómeno se producirá al mezclar el vinagre con el bicarbonato?",
                    "hypothesis_options": [
                        "No habrá ningún cambio observable.",
                        "Se producirá una reacción efervescente con abundante espuma y gas.",
                        "El líquido se congelará instantáneamente."
                    ],
                    "correct_hypothesis": "Se producirá una reacción efervescente con abundante espuma y gas.",
                    "explanation": "Al juntar el vinagre (un ácido) con el bicarbonato (una base), se produce una reacción química que libera gas dióxido de carbono en forma de espuma."
                }
            ),
            (
                3,
                "Clasificación de Animales: Vertebrados e Invertebrados",
                "Clasifica los 6 animales según la presencia o ausencia de columna vertebral.",
                "category_sort",
                "1f985",
                {
                    "categories": [
                        {"id": "c1", "name": "Animales Vertebrados"},
                        {"id": "c2", "name": "Animales Invertebrados"}
                    ],
                    "elements": [
                        {"id": "e1", "name": "Perro", "category_id": "c1", "icon_code": "1f436"},
                        {"id": "e2", "name": "Gato", "category_id": "c1", "icon_code": "1f431"},
                        {"id": "e3", "name": "Águila", "category_id": "c1", "icon_code": "1f985"},
                        {"id": "e4", "name": "Gusano", "category_id": "c2", "icon_code": "1fab1"},
                        {"id": "e5", "name": "Mariposa", "category_id": "c2", "icon_code": "1f98b"},
                        {"id": "e6", "name": "Caracol", "category_id": "c2", "icon_code": "1f40c"}
                    ]
                }
            ),
            (
                4,
                "Clasificación del Ecosistema: Seres Vivos e Inertes",
                "Organiza los 6 elementos del entorno natural entre seres vivos (bióticos) y seres inertes (abióticos).",
                "category_sort",
                "1f30d",
                {
                    "categories": [
                        {"id": "c1", "name": "Seres Vivos (Bióticos)"},
                        {"id": "c2", "name": "Objetos Inertes (Abióticos)"}
                    ],
                    "elements": [
                        {"id": "e1", "name": "Árbol de roble", "category_id": "c1", "icon_code": "1f333"},
                        {"id": "e2", "name": "Rana", "category_id": "c1", "icon_code": "1f438"},
                        {"id": "e3", "name": "Hongo champiñón", "category_id": "c1", "icon_code": "1f344"},
                        {"id": "e4", "name": "Roca", "category_id": "c2", "icon_code": "1faa8"},
                        {"id": "e5", "name": "Agua de río", "category_id": "c2", "icon_code": "1f4a7"},
                        {"id": "e6", "name": "Aire", "category_id": "c2", "icon_code": "1f4a8"}
                    ]
                }
            ),
            (
                5,
                "Alimentación Saludable y Cuidado Ambiental",
                "Clasifica cada elemento en su tabla correspondiente: Alimentos Saludables, Ultraprocesados o Materiales Reciclables.",
                "category_sort",
                "267b",
                {
                    "categories": [
                        {"id": "saludable", "name": "Alimentos Saludables"},
                        {"id": "ultraprocesado", "name": "Ultraprocesados"},
                        {"id": "reciclable", "name": "Materiales Reciclables"}
                    ],
                    "elements": [
                        {"id": "a1", "name": "Manzana fresca", "category_id": "saludable", "icon_code": "1f34e"},
                        {"id": "a2", "name": "Brócoli", "category_id": "saludable", "icon_code": "1f966"},
                        {"id": "a3", "name": "Refresco azucarado", "category_id": "ultraprocesado", "icon_code": "1f964"},
                        {"id": "a4", "name": "Papas fritas de bolsa", "category_id": "ultraprocesado", "icon_code": "1f35f"},
                        {"id": "a5", "name": "Botella de vidrio", "category_id": "reciclable", "icon_code": "1f37e"},
                        {"id": "a6", "name": "Caja de cartón", "category_id": "reciclable", "icon_code": "1f4e6"}
                    ]
                }
            ),
        ]

        for num, title, inst, atype, icon, extra in primaria_science_items:
            Activity.objects.update_or_create(
                workbook=wb_primaria_science,
                activity_number=num,
                defaults={
                    'title': title,
                    'instruction': inst,
                    'activity_type': atype,
                    'visual_emoji': icon,
                    'prompt_text': '',
                    'options': '',
                    'correct_answer': 'COMPLETADO',
                    'extra_data': extra,
                }
            )

        self.stdout.write(self.style.SUCCESS("¡Actividades de Inicial y Primaria (Lenguaje, Matemáticas y Ciencias) cargadas exitosamente!"))