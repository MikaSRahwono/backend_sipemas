#!/bin/sh

# Wait for the database to be ready
while ! pg_isready -h $DB_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Waiting for database..."
  sleep 2
done

echo "Running Database Migrations"
python manage.py makemigrations --settings=backend_sipemas.settings.stage

python manage.py migrate --settings=backend_sipemas.settings.stage

python manage.py loaddata api/user/fixtures/organization.json --settings=backend_sipemas.settings.stage

python manage.py seed_groups --settings=backend_sipemas.settings.stage

echo "Running app1 management commands"
python manage.py sample_management_command

exec "$@"