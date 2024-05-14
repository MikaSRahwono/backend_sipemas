#!/bin/sh

echo "Running Database Migrations"
python manage.py makemigrations --settings=backend_sipemas.settings.stage

python manage.py migrate --settings=backend_sipemas.settings.stage

python manage.py loaddata api/user/fixtures/organization.json --settings=backend_sipemas.settings.stage

python manage.py seed_groups --settings=backend_sipemas.settings.stage

exec "$@"