from rest_framework import serializers
from django.db.models import Q

from api.academic.models import AssignmentComponent, Course
from api.academic.serializers import AssignmentComponentSerializer, CourseSerializer, StepAssignmentSerializer
from api.activity.models import Activity, FileSubmission, LogSubmission
from api.activity.serializers import ActivitySerializer, FileSubmissionSerializer, LogSubmissionSerializer, StepCompletionSerializer, SuperviseesSerializer
from api.dashboard.models import Note
from api.marketplace.models import Application, ApplicationApproval
from api.marketplace.serializers import SupervisorSerializer, TopicListSerializer
from api.user.serializers import UserDetailSerializer, UserProfileSerializer
from api.user.models import User

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentComponent
        fields = '__all__'

class StudentActivitySerializer(serializers.ModelSerializer):
    supervisors = SupervisorSerializer(read_only=True, many=True)
    supervisees = SuperviseesSerializer(read_only=True, many=True)

    file_submissions = FileSubmissionSerializer(source='filesubmissions', read_only=True, many=True)
    log_submissions = LogSubmissionSerializer(source='logsubmissions', read_only=True, many=True)
    step_completion = StepCompletionSerializer(source='stepcompletions', read_only=True, many=True)

    topic = TopicListSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

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
        data['activities_count'] = len(activities)

        not_all_approved_application_approvals = ApplicationApproval.objects.filter(
            Q(approvee=lecturer) &
            (Q(approval_status=0) | Q(approval_status=1))
        )
        data['approval_pending'] = len(not_all_approved_application_approvals)

        count_per_activities = []
        courses = Course.objects.all()

        for course in courses:
            activities_per_course = Activity.objects.filter(supervisors=lecturer, course=course)
            data_count = {
                'course': course.nm_mk,
                'count': len(activities_per_course)
            }
            count_per_activities.append(data_count)
        
        data['acitivites_count_courses'] = count_per_activities
        return data