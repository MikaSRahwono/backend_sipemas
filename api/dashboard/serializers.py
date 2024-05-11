from rest_framework import serializers
from django.db.models import Q

from api.academic.models import AssignmentComponent, Course
from api.academic.serializers import AssignmentComponentSerializer, CourseSerializer, StepAssignmentSerializer
from api.activity.models import Activity, FileSubmission, LogSubmission
from api.activity.serializers import ActivitySerializer, FileSubmissionSerializer, LogSubmissionSerializer, StepCompletionSerializer, SuperviseesSerializer
from api.dashboard.models import Note
from api.marketplace.models import Application, ApplicationApproval, Topic, TopicRequest, TopicRequestApproval
from api.marketplace.serializers import SupervisorSerializer, TopicListSerializer, TopicRequestApprovalSerializer, TopicRequestSerializer
from api.user.serializers import UserDetailSerializer, UserProfileSerializer
from api.user.models import User

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentComponent
        fields = '__all__'

class StudentActivitySerializer(serializers.ModelSerializer):
    supervisors = SupervisorSerializer(read_only=True, many=True)
    supervisees = SuperviseesSerializer(read_only=True, many=True)

    step_completion = StepCompletionSerializer(source='stepcompletions', read_only=True, many=True)

    topic = TopicListSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        assignment_components = AssignmentComponent.objects.filter(
            step_component__activity_step__course__kd_mk=instance.course.kd_mk
        )

        assignments_data = []
        for assignment in assignment_components:
            if assignment.type == "LOG":
                log_submissions = LogSubmission.objects.filter(activity__id=instance.id, assignment_component=assignment)
                serializer = LogSubmissionSerializer(log_submissions, many=True)
                assignment_serializer = AssignmentComponentSerializer(assignment)
                assignment_submission = {
                    'assignment_component': assignment_serializer.data,
                    'data': serializer.data
                }
                assignments_data.append(assignment_submission)

            elif assignment.type == "SUB":
                file_submission = FileSubmission.objects.filter(activity__id=instance.id, assignment_component=assignment).first()
                serializer = FileSubmissionSerializer(file_submission)
                assignment_serializer = AssignmentComponentSerializer(assignment)
                assignment_submission = {
                    'assignment_component': assignment_serializer.data,
                    'data': serializer.data
                }
                assignments_data.append(assignment_submission)

        data['assignments'] = assignments_data

        return data

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'creator', 'activity',)

class LecturerDataSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lecturer = User.objects.get(id=instance.id)

        activities = Activity.objects.filter(supervisors=lecturer)
        activity_serializer = ActivitySerializer(activities, many=True)
        data['activities_count'] = len(activities)
        data['supervised_activity'] = activity_serializer.data

        not_all_approved_application_approvals = ApplicationApproval.objects.filter(
            Q(approvee=lecturer) &
            (Q(approval_status=0) | Q(approval_status=1))
        )
        not_all_approved_topic_requests_approvals = TopicRequestApproval.objects.filter(
            Q(approvee=lecturer) &
            (Q(approval_status=0) | Q(approval_status=1))
        )
        data['approval_pending'] = len(not_all_approved_application_approvals) + len(not_all_approved_topic_requests_approvals)
        
        topic_request_approvals = []
        for topic_request_approval in not_all_approved_topic_requests_approvals:
            topic_request_serializer = TopicRequestApprovalSerializer(topic_request_approval)
            topic_request_approvals.append(topic_request_serializer.data)

        data['topic_request_approvals'] = topic_request_approvals

        topics = Topic.objects.filter(supervisors=lecturer)
        topic_serializer = TopicListSerializer(topics, many=True)
        data['supervised_topics_count'] = len(topics)
        data['supervised_topics'] = topic_serializer.data

        count_per_activities = []
        courses = Course.objects.all()

        for course in courses:
            activities_per_course = Activity.objects.filter(supervisors=lecturer, course=course)
            data_count = {
                'course': course.nm_mk,
                'count': len(activities_per_course)
            }
            count_per_activities.append(data_count)
        
        data['activites_count_courses'] = count_per_activities
        return data


class StudentDataSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student = User.objects.get(id=instance.id)

        activity = Activity.objects.filter(supervisees=student, is_completed=None).first()
        data['currently_taken_course'] = activity.course.nm_mk

        topic_requests_created = TopicRequest.objects.filter(
            Q(creator=student)
        )
        topic_requested_approvals = TopicRequestApproval.objects.filter(
            Q(approvee=student)
        )

        topic_requested = []
        for topic_request in topic_requests_created:
            topic_request_serializer = TopicRequestSerializer(topic_request)
            topic_requested.append(topic_request_serializer.data)
        for approval in topic_requested_approvals:
            topic_request_serializer = TopicRequestSerializer(approval.topic_request)
            topic_requested.append(topic_request_serializer.data)
        
        data['topic_requested_count'] = len(topic_requested) + len(topic_requests_created)
        data['topic_requested'] = topic_requested

        activities = Activity.objects.filter(supervisees=student, is_completed=None)
        activity_serializer = ActivitySerializer(activities, many=True)
        data ['active_activity'] = activity_serializer.data

        return data
    