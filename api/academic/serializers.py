from api.user.serializers import OrganizationSerializer
from rest_framework import serializers
from .models import *

class CourseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInformation
        fields = ['html']

class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisiteSerializer(many=True, read_only=True)
    allowed_organizations = OrganizationSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('kd_mk',)

    def create(self,validated_data):
        allowed_organizations = self.initial_data['allowed_organizations']
        organizationInstances = []
        
        for organization in allowed_organizations:
            organizationInstances.append(Organization.objects.get(id = organization['id']))
        course = Course.objects.create(**validated_data)
        course.allowed_organizations.set(organizationInstances)
        
        return course
    
    def update(self, instance, validated_data):
        allowed_organizations = self.initial_data['allowed_organizations']
        organizationInstances = []
        
        for organization in allowed_organizations:
            organizationInstances.append(Organization.objects.get(id = organization['id']))
        instance.allowed_organizations.set(organizationInstances) 

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class InformationComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationComponent
        fields = ['id', 'heading', 'subheading', 'paragraph']

class AnnouncementComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementComponent
        fields = ['id', 'heading', 'subheading', 'paragraph']

class AssignmentComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentComponent
        fields = ['id', 'title', 'subtitle', 'description', 'type']

class StepComponentSerializer(serializers.ModelSerializer):
    information_component = InformationComponentSerializer(source='informationcomponents', read_only=True)
    announcement_component = AnnouncementComponentSerializer(source='announcementcomponents', many=True, read_only=True)
    assignment_component = AssignmentComponentSerializer(source='assignmentcomponents', read_only=True)

    class Meta:
        model = StepComponent
        fields = ['id', 'index', 'type', 'information_component', 'announcement_component', 'assignment_component']

class StepInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepInformation
        fields = ['id', 'heading', 'subheading', 'html']

class StepSidangSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepSidang
        fields = ['id', 'heading', 'subheading', 'paragraph']

class StepAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepAssignment
        fields = ['id', 'heading', 'subheading']

class ActivityStepSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    step_information = StepInformationSerializer(source='stepinformation', read_only=True)
    step_sidang = StepSidangSerializer(source='stepsidang', read_only=True)
    step_assignment = StepAssignmentSerializer(source='stepassignment', read_only=True)

    components = StepComponentSerializer(source='stepcomponents', read_only=True, many=True)

    class Meta:
        model = ActivityStep
        fields = ['id', 'course', 'index', 'name', 'type', 'step_information', 'step_sidang', 'step_assignment', 'components']
