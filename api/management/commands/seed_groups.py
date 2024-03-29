from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Seed default groups in the database'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Lecturer')
        Group.objects.get_or_create(name='Student')
        Group.objects.get_or_create(name='Secretary')

