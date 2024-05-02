from api.marketplace.serializers import SupervisorSerializer, UserDetailSerializer, UserProfileSerializer
from rest_framework import serializers
from .models import *

class LogSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSubmission
        fields = ['subject', 'body', 'assignment_component', 'created_on', 'updated_on', 'deleted_on']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class FileSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSubmission
        fields = ['subject', 'body', 'file', 'created_on', 'updated_on', 'deleted_on']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class StepCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepCompletion
        fields = '__all__'
        read_only_fields = ('activity', 'activity_step', 'is_completed', 'created_on', 'updated_on', 'deleted_on')

class SuperviseeSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']

class ActivitySerializer(serializers.ModelSerializer):
    step_completion = StepCompletionSerializer(source='stepcompletions', read_only=True)
    log_submissions = LogSubmissionSerializer(source='logsubmissions', read_only=True)
    file_submissions = FileSubmissionSerializer(source='filesubmissions', read_only=True)

    supervisors = SupervisorSerializer(read_only=True, many=True)
    supervisee = SuperviseeSerializer(read_only=True, many=True)

    class Meta:
        model = Activity
        fields = '__all__'
