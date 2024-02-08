# store/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import *

@receiver(post_save, sender=Application)
def create_product_confirmation(sender, user, application, **kwargs):
    approvee = user
    application = application
    ApplicationApproval.objects.create(approvee=user, application=application)


application_creation_done = Signal()

@receiver(application_creation_done)
def handle_application_creation_done(sender, users_data_list, application, **kwargs):
    for users_data in users_data_list:
        user_id = users_data.pop('id', None)
        user = User.objects.get(pk=user_id)
        create_product_confirmation(sender=Application, user_instance=user, application=application)