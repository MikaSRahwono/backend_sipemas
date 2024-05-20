from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from django.db.models import Q

from .models import Application, Topic, TopicInformation, TopicRequest, TopicRequestApproval
from .models import ApplicationApproval
from ..activity.models import Activity

create_request_approval_signal = Signal()
@receiver(create_request_approval_signal)
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
    
    def restrict_other_requests(supervisee):
        topic_request_approvals = TopicRequestApproval.objects.filter(approvee=supervisee)
        application_approvals = ApplicationApproval.objects.filter(approvee=supervisee)

        for approval in topic_request_approvals:
            if (approval.approval_status == 0 or approval.approval_status == 1) and approval.topic_request != topic_request:
                approval.topic_request.is_approved = False
                approval.approval_status = 3
                approval.save()
                approval.topic_request.save()

        for approval in application_approvals:
            if approval.approval_status == 0 or approval.approval_status == 1:
                approval.application.is_approved = False
                approval.approval_status = 3
                approval.save()
                approval.application.save()


    topic_request_approval = TopicRequestApproval.objects.get(id=topic_request_approval.id)
    topic_request_approval.approval_status = 1
    topic_request_approval.save()

    topic_request = topic_request_approval.topic_request

    if topic_request.is_approved == False:
        return
    
    all_approved = not topic_request.topicrequestapproval_set.filter(Q(is_approved=False) | Q(is_approved__isnull=True)).exists()
    is_no_restricted = not topic_request.topicrequestapproval_set.filter(Q(approval_status=-1) | Q(approval_status=0) | Q(approval_status=2) | Q(approval_status=3)).exists()

    if all_approved and is_no_restricted:     
        topic_request.is_approved = True
        topic_request.save()
        topic_request.course.topic_count += 1
        topic_request.course.save()
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

        topic_information = TopicInformation.objects.create(
            topic = topic,
            html = "<p>" + topic_request.description + "</p>"
        )

        activity.supervisees.add(topic_request.creator)
        if topic_request.applicants:
            activity.supervisees.add(*topic_request.applicants.all())
        activity.supervisors.add(*topic_request.supervisors.all())
        activity.save()

        if topic_request.course.course_type == 'OO':
            restrict_other_requests(user)
            for supervisee in activity.supervisees.all():
                restrict_other_requests(supervisee)

        topic_request_approvals = TopicRequestApproval.objects.filter(topic_request=topic_request)

        for approval in topic_request_approvals:
            approval.approval_status = 2
            approval.save()
        
        activity.save()

create_application_approval_signal = Signal()
@receiver(create_application_approval_signal)
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
    
    def restrict_other_requests(supervisee):
        topic_request_approvals = TopicRequestApproval.objects.filter(approvee=supervisee)
        application_approvals = ApplicationApproval.objects.filter(approvee=supervisee)

        for approval in topic_request_approvals:
            if approval.approval_status == 0 or approval.approval_status == 1:
                approval.topic_request.is_approved = False
                approval.approval_status = 3
                approval.save()
                approval.topic_request.save()

        for approval in application_approvals:
            if (approval.approval_status == 0 or approval.approval_status == 1) and approval.application != application:
                approval.application.is_approved = False
                approval.approval_status = 3
                approval.save()
                approval.application.save()


    application_approval = ApplicationApproval.objects.get(id=application_approval.id)
    application_approval.approval_status = 1
    application_approval.save()

    application = application_approval.application

    if application.is_approved == False:
        return
    
    all_approved = not application.applicationapproval_set.filter(Q(is_approved=False) | Q(is_approved__isnull=True)).exists()
    is_no_restricted = not application.applicationapproval_set.filter(Q(approval_status=-1) | Q(approval_status=0) | Q(approval_status=2) | Q(approval_status=3)).exists()

    if all_approved and is_no_restricted:     
        application.is_approved = True
        application.save()
        activity = Activity.objects.create(
            topic = application.topic,
            course = application.topic.course,
            application=application
        )
        
        activity.supervisees.add(application.creator)
        if application.applicants:
            activity.supervisees.add(*application.applicants.all())
        activity.supervisors.add(*application.topic.supervisors.all())

        if application.topic.course.course_type == 'OO':
            restrict_other_requests(user)
            for supervisee in activity.supervisees.all():
                restrict_other_requests(supervisee)

        application_application_approvals = ApplicationApproval.objects.filter(application=application)

        for approval in application_application_approvals:
            approval.approval_status = 2
            approval.save()
        
        activity.save()

