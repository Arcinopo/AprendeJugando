from django.contrib import admin
from django.utils.html import format_html
from .models import Workbook, Activity, ActivityProgress, Drawing

# Personalización de títulos del Dashboard Admin
admin.site.site_header = "AprendeJugando · Panel de Administración"
admin.site.site_title = "Admin AprendeJugando"
admin.site.index_title = "Gestión de Contenidos, Alumnos y Galería"


class ActivityInline(admin.TabularInline):
    """Permite agregar o editar actividades directamente dentro de un Cuadernillo."""
    model = Activity
    extra = 1
    fields = ('activity_number', 'title', 'activity_type', 'visual_emoji', 'prompt_text', 'options', 'correct_answer')


@admin.register(Workbook)
class WorkbookAdmin(admin.ModelAdmin):
    list_display = ('order', 'icon_preview', 'title', 'category', 'activities_count')
    list_display_links = ('title',)
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title', 'description')
    inlines = [ActivityInline]

    def icon_preview(self, obj):
        if obj.emoji_icon:
            return format_html(
                '<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{}.svg" width="28" height="28" />',
                obj.emoji_icon
            )
        return "-"
    icon_preview.short_description = "Icono"

    def activities_count(self, obj):
        return obj.activities.count()
    activities_count.short_description = "Nº Actividades"


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_number', 'title', 'workbook', 'activity_type', 'visual_preview', 'correct_answer')
    list_display_links = ('title',)
    list_filter = ('workbook', 'activity_type')
    search_fields = ('title', 'instruction', 'prompt_text')
    ordering = ('workbook', 'activity_number')

    def visual_preview(self, obj):
        icons = obj.get_visual_icons()
        if not icons:
            return "-"
        html = "".join([
            f'<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{code}.svg" width="24" height="24" style="margin-right:4px;" />'
            for code in icons
        ])
        return format_html(html)
    visual_preview.short_description = "Ilustración"


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'user', 'created_at')
    list_display_links = ('thumbnail_preview', 'title')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user__username', 'user__first_name')
    readonly_fields = ('large_preview', 'created_at')

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:65px; height:50px; object-fit:contain; background:#fff; border:1px solid #ddd; border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    thumbnail_preview.short_description = "Miniatura"

    def large_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="max-width:350px; border:2px solid #ccc; border-radius:10px; background:#fff;" /></a>',
                obj.image.url
            )
        return "Sin imagen"
    large_preview.short_description = "Vista previa en Cloudinary"


@admin.register(ActivityProgress)
class ActivityProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'completed', 'completed_at')
    list_filter = ('completed', 'activity__workbook', 'user')
    search_fields = ('user__username', 'user__first_name', 'activity__title')