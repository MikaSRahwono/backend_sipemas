from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Application
from .models import ApplicationApproval

@receiver(m2m_changed, sender=Application.applicants.through)
def create_application_approval(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        for supervisor in instance.topic.supervisors.all():
            approval_instance = ApplicationApproval(application=instance, approvee=supervisor, is_supervisor=True)
            approval_instance.save()
        for applicant in instance.applicants.all():
            approval_instance = ApplicationApproval(application=instance, approvee=applicant)
            approval_instance.save()