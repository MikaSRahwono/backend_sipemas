from rest_framework import serializers

from api.academic.models import AssignmentComponent
from api.academic.serializers import AssignmentComponentSerializer, StepAssignmentSerializer
from api.activity.models import Activity, FileSubmission, LogSubmission
from api.activity.serializers import SuperviseesSerializer
from api.marketplace.serializers import SupervisorSerializer, TopicListSerializer

class LogSubmissionSerializer(serializers.ModelSerializer):
    assignment_component = AssignmentComponentSerializer()

    class Meta:
        model = LogSubmission
        fields = ['id','subject', 'body', 'assignment_component', 'created_on', 'updated_on', 'deleted_on']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class FileSubmissionSerializer(serializers.ModelSerializer):
    assignment_component = AssignmentComponentSerializer()

    class Meta:
        model = FileSubmission
        fields = ['id','subject', 'body', 'file', 'created_on', 'updated_on', 'deleted_on', 'assignment_component']
        read_only_fields = ('created_on', 'updated_on', 'deleted_on', 'assignment_component',)

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentComponent
        fields = '__all__'

class StudentActivitySerializer(serializers.ModelSerializer):
    supervisors = SupervisorSerializer(read_only=True, many=True)
    supervisees = SuperviseesSerializer(read_only=True, many=True)

    file_submissions = FileSubmissionSerializer(source='filesubmissions', read_only=True, many=True)
    log_submissions = LogSubmissionSerializer(source='logsubmissions', read_only=True, many=True)

    topic = TopicListSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'
