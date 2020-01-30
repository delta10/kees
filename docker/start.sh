#!/usr/bin/env sh
set -e

# Collect static
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start server
uwsgi --http :8000 --module kees.wsgi --processes 4 --threads 2 --static-map /static=/app/static --static-map /media=/app/media
