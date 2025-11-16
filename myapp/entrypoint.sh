#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn myapp.wsgi:application --bind 0.0.0.0:$PORT
