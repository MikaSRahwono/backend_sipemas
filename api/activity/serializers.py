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

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
