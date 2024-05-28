import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'backend_sipemas.settings.stage')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SUPERUSER_USERNAME'],
        os.environ['DJANGO_SUPERUSER_EMAIL'],
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")

