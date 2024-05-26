#!/bin/sh

if [ -z "$ALLOWED_HOSTS" ]; then
  echo "Error: ALLOWED_HOSTS environment variable is not set."
  exit 1
fi

echo "Running Database Migrations"
python manage.py makemigrations --settings=backend_sipemas.settings.stage

python manage.py migrate --settings=backend_sipemas.settings.stage

python manage.py loaddata api/user/fixtures/organization.json --settings=backend_sipemas.settings.stage

python manage.py seed_groups --settings=backend_sipemas.settings.stage

python manage.py collectstatic --noinput --settings=backend_sipemas.settings.stage

python create_superuser.py

exec gunicorn backend_sipemas.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=backend_sipemas.settings.stage
