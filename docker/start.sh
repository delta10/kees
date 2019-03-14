#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
uwsgi --http :8000 --uid www-data --gid www-data --module kees.wsgi --static-map /static=/app/static --static-map /media=/app/media
