from django.contrib import admin
from .models import EmailVerificationCode


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'attempts', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('attempts', 'created_at')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Correo"