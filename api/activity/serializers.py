from api.academic.serializers import CourseSerializer
from api.marketplace.serializers import SupervisorSerializer, TopicListSerializer, UserDetailSerializer, UserProfileSerializer
from rest_framework import serializers
from .models import *

class LogSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSubmission
        fields = ['id','subject', 'body', 'assignment_component', 'created_on', 'updated_on', 'deleted_on']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class FileSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSubmission
        fields = ['id','subject', 'body', 'file', 'created_on', 'updated_on', 'deleted_on', 'assignment_component']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class StepCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepCompletion
        fields = '__all__'
        read_only_fields = ('activity', 'activity_step', 'is_completed', 'created_on', 'updated_on', 'deleted_on')

class SuperviseesSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']

class ActivitySerializer(serializers.ModelSerializer):
    supervisors = SupervisorSerializer(read_only=True, many=True)
    supervisees = SuperviseesSerializer(read_only=True, many=True)

    step_completion = StepCompletionSerializer(source='stepcompletions', read_only=True, many=True)

    topic = TopicListSerializer(read_only=True)

    course = CourseSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'
