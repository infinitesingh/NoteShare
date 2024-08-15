#!/bin/sh

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the application
exec gunicorn NoteShare.wsgi:application --bind 0.0.0.0:8000