#!/bin/bash

# Run created migrations
python3 manage.py migrate

# Do not prompt the user for input of any kind (https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/)
python3 manage.py collectstatic --no-input

gunicorn --reload -w 3 -b 0.0.0.0:8000 auth_service.wsgi:application