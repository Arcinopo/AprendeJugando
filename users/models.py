import secrets
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmailVerificationCode(models.Model):
    MAX_ATTEMPTS = 5

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6)
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def generate_new_code(self):
        self.code = f"{secrets.randbelow(900000) + 100000}"
        self.attempts = 0
        self.save()
        return self.code

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def register_failed_attempt(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])
        return self.attempts >= self.MAX_ATTEMPTS

    def __str__(self):
        return f"Verificación pendiente para {self.user.email}"