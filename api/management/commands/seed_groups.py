from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Seed default groups in the database'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Lecturer')
        Group.objects.get_or_create(name='Student')
        Group.objects.get_or_create(name='Secretary')
        Group.objects.get_or_create(name='Manager')
        Group.objects.get_or_create(name='01.00.12.01')
        Group.objects.get_or_create(name='02.00.12.01')
        Group.objects.get_or_create(name='03.00.12.01')
        Group.objects.get_or_create(name='04.00.12.01')
        Group.objects.get_or_create(name='05.00.12.01')
        Group.objects.get_or_create(name='06.00.12.01')
        Group.objects.get_or_create(name='07.00.12.01')
        Group.objects.get_or_create(name='08.00.12.01')
        Group.objects.get_or_create(name='09.00.12.01')

