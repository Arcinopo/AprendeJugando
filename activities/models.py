from django.db import models
from django.contrib.auth.models import User


class Workbook(models.Model):
    CATEGORY_CHOICES = [
        ('lectoescritura', 'Lectoescritura y Vocales'),
        ('comprension', 'Comprensión Lectora y Lenguaje'),
        ('matematica', 'Matemáticas Divertidas'),
        ('ciencias', 'Ciencias y Experimentos'),
        ('creatividad', 'Creatividad y Arte'),
        ('cuentos', 'Cuentos y Canciones'),
        ('motricidad', 'Motricidad y Trazos'),
    ]

    GRADE_CHOICES = [
        ('todos', 'Todos los niveles'),
        ('inicial', 'Preescolar / Inicial'),
        ('primaria', 'Primaria'),
    ]

    title = models.CharField(max_length=120, verbose_name="Título del Cuadernillo")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='lectoescritura')
    grade_level = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        default='todos',
        verbose_name="Nivel educativo",
    )
    description = models.TextField(blank=True)
    emoji_icon = models.CharField(max_length=10, default="1f4da")
    color_theme = models.CharField(
        max_length=20,
        default="primary",
        help_text="Clase Bootstrap: primary, success, warning, info, danger",
    )
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name = "Cuadernillo"
        verbose_name_plural = "Cuadernillos"

    def __str__(self):
        return f"{self.title} ({self.get_grade_level_display()})"


class Activity(models.Model):
    ACTIVITY_TYPES = [
        # Tipos existentes
        ('fill_vowel', 'Completar Vocal o Sílaba'),
        ('match_pair', 'Seleccionar / Unir Opción Correcta'),
        ('math_count', 'Conteo y Números'),
        ('drawing_prompt', 'Reto de Dibujo en Pizarra'),
        # Nuevos tipos para Primaria y Ciencias
        ('error_hunter', 'Cazadores de Errores (Ortografía y Lógica)'),
        ('comic_fill', 'Completar el Cómic'),
        ('word_search', 'Sopa de Letras / Crucigrama'),
        ('math_maze', 'Laberinto Numérico'),
        ('visual_sudoku', 'Sudoku Visual'),
        ('spot_differences', 'Encuentra las Diferencias'),
        ('math_problem', 'Problema Matemático Contextualizado'),
        ('science_experiment', 'Experimento Casero y Ficha'),
        ('category_sort', 'Clasificación por Categorías'),
    ]

    workbook = models.ForeignKey(Workbook, on_delete=models.CASCADE, related_name='activities')
    activity_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150)
    instruction = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES, default='fill_vowel')

    # Datos dinámicos del ejercicio
    visual_emoji = models.CharField(
        max_length=100,
        blank=True,
        help_text="Códigos Twemoji separados por coma. Ej: 2708, 1f418",
    )
    prompt_text = models.TextField(
        blank=True,
        help_text="Consigna, lectura corta, problema o texto con errores",
    )
    options = models.TextField(
        blank=True,
        help_text="Opciones separadas por coma. Ej: A,E,I,O,U",
    )
    correct_answer = models.CharField(
        max_length=255,
        blank=True,
        help_text="Respuesta exacta esperada",
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuración estructurada para sopa de letras, laberintos, sudokus, cómics y experimentos",
    )

    class Meta:
        ordering = ['workbook', 'activity_number']
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def get_options_list(self):
        if not self.options:
            return []
        return [opt.strip() for opt in self.options.split(',')]

    def get_visual_icons(self):
        if not self.visual_emoji:
            return []
        return [code.strip() for code in self.visual_emoji.split(',')]

    def __str__(self):
        return f"Act. {self.activity_number}: {self.title}"


class ActivityProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_progress')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"


class Drawing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drawings')
    title = models.CharField(max_length=100, default="Mi Obra de Arte")
    # MediaCloudinaryStorage subirá automáticamente este campo a Cloudinary
    image = models.ImageField(upload_to='kids_drawings/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Dibujo"
        verbose_name_plural = "Dibujos"

    def __str__(self):
        return f"{self.title} ({self.user.username})"