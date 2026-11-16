import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad: exige SECRET_KEY explícita en el entorno (sin respaldo inseguro)
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos y orígenes confiables CSRF para Render
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000', cast=Csv())

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'cloudinary_storage',
    'cloudinary',

    'users',
    'activities',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Base de datos única (Neon PostgreSQL)
DATABASE_URL = config('DATABASE_URL', default='')
if not DATABASE_URL:
    raise ImproperlyConfigured("La variable de entorno DATABASE_URL es obligatoria.")

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
]

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (WhiteNoise)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Almacenamiento Django 5.x (WhiteNoise + Cloudinary)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': config('CLOUDINARY_URL', default='')
}
if not DEBUG and not CLOUDINARY_STORAGE['CLOUDINARY_URL']:
    raise ImproperlyConfigured("CLOUDINARY_URL es obligatoria en producción.")

MEDIA_URL = '/media/'

# Redirecciones de Autenticación
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'activities:home'
LOGOUT_REDIRECT_URL = 'users:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguridad HTTPS y HSTS en Producción (Render)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- CONFIGURACIÓN DE CORREO ELECTRÓNICO (BREVO / SMTP) ---
# --- CONFIGURACIÓN DE CORREO ELECTRÓNICO (BREVO API HTTPS) ---
BREVO_API_KEY = config('BREVO_API_KEY', default='').strip()
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='').strip()

if not DEBUG and (not BREVO_API_KEY or not DEFAULT_FROM_EMAIL):
    raise ImproperlyConfigured(
        "Faltan credenciales de correo (BREVO_API_KEY, DEFAULT_FROM_EMAIL) con DEBUG=False."
    )