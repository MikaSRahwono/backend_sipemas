from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from .models import Application
from .models import ApplicationApproval
from ..activity.models import Activity

@receiver(m2m_changed, sender=Application.applicants.through)
def create_application_approval(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        for supervisor in instance.topic.supervisors.all():
            approval_instance = ApplicationApproval(application=instance, approvee=supervisor, is_supervisor=True)
            approval_instance.save()
        for applicant in instance.applicants.all():
            approval_instance = ApplicationApproval(application=instance, approvee=applicant)
            approval_instance.save()

application_approved_signal = Signal()

@receiver(application_approved_signal)
def handle_application_approved(sender, application_approval, user, **kwargs):
    application = application_approval.application
    all_approved = not application.applicationapproval_set.filter(is_approved=False).exists()

    if all_approved:
        application.is_approved = True
        application.save()
        activity = Activity.objects.create(
            topic = application.topic,
            course = application.topic.course,
            application=application
        )
        activity.supervisee.add(application.user)
        activity.supervisee.add(*application.applicants.all())
        activity.supervisor.add(*application.topic.supervisors.all())
        activity.save()