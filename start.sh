#!/bin/bash
python manage.py migrate
gunicorn MANJARESCAMPO.wsgi:application --bind 0.0.0.0:$PORT