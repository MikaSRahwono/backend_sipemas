from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from django.db.models import Q

from .models import Application, Topic, TopicRequest, TopicRequestApproval
from .models import ApplicationApproval
from ..activity.models import Activity

@receiver(m2m_changed, sender=TopicRequest.supervisors.through)
def create_request_approval(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        for supervisor in instance.supervisors.all():
            approval_instance = TopicRequestApproval(topic_request=instance, approvee=supervisor, is_supervisor=True)
            approval_instance.save()
        for applicant in instance.applicants.all():
            approval_instance = TopicRequestApproval(topic_request=instance, approvee=applicant)
            approval_instance.save()

topic_request_approved_signal = Signal()

@receiver(topic_request_approved_signal)
def handle_topic_request_approved(sender, topic_request_approval, user, **kwargs):
    topic_request = topic_request_approval.topic_request
    all_approved = not topic_request.topicrequestapproval_set.filter(Q(is_approved=False) | Q(is_approved__isnull=True)).exists()

    if all_approved:
        topic_request.is_approved = True
        topic_request.save()
        topic = Topic.objects.create(
            course = topic_request.course,
            title = topic_request.title,
            is_open = False,
            num_of_people = topic_request.num_of_people,
            created_on = topic_request.created_on,
            creator = topic_request.creator
        )
        topic.supervisors.add(*topic_request.supervisors.all())
        topic.fields.add(*topic_request.fields.all())

        activity = Activity.objects.create(
            topic = topic,
            course = topic.course,
            topic_request=topic_request
        )

        activity.supervisees.add(topic_request.creator)
        activity.supervisees.add(*topic_request.applicants.all())
        activity.supervisors.add(*topic_request.supervisors.all())
        activity.save()

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
    all_approved = not application.applicationapproval_set.filter(Q(is_approved=False) | Q(is_approved__isnull=True)).exists()

    if all_approved:
        application.is_approved = True
        application.save()
        activity = Activity.objects.create(
            topic = application.topic,
            course = application.topic.course,
            application=application
        )
        activity.supervisees.add(application.user)
        activity.supervisees.add(*application.applicants.all())
        activity.supervisors.add(*application.topic.supervisors.all())
        activity.save()