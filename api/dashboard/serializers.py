from rest_framework import serializers

from api.academic.models import AssignmentComponent
from api.academic.serializers import AssignmentComponentSerializer, StepAssignmentSerializer
from api.activity.models import Activity, FileSubmission, LogSubmission
from api.activity.serializers import FileSubmissionSerializer, LogSubmissionSerializer, StepCompletionSerializer, SuperviseesSerializer
from api.marketplace.serializers import SupervisorSerializer, TopicListSerializer

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

    class Meta:
        model = Activity
        fields = '__all__'
