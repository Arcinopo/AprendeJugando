#!/usr/bin/env bash
# Salir inmediatamente si ocurre algún error
set -o errexit

pip install -r requirements.txt

# Recolectar archivos estáticos (CSS, JS, audios mp3) para WhiteNoise
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos PostgreSQL en Neon
python manage.py migrate

# Poblar la base de datos con las actividades de los cuadernillos (idempotente)
python manage.py seed_activities