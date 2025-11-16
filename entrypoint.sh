#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicron myapp.wsgi:application --bind 0.0.0.0:$PORT
