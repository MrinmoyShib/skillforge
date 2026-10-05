#!/bin/sh
set -e

if [ "$ENVIRONMENT" = "production" ] || [ "$DJANGO_SETTINGS_MODULE" = "config.settings.prod" ]; then
    echo "==> [SkillForge] Launching Gunicorn WSGI server for production..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2
else
    echo "==> [SkillForge] Launching Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
fi

