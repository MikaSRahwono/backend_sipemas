from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from ..user.serializers import UserDetailSerializer, UserProfileSerializer, UserSerializer
from ..academic.serializers import CourseSerializer

class TopicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicInformation
        fields = ['html']

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class SupervisorSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']

class ApplicantsSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']

class TopicListSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    fields = FieldSerializer(read_only=True, many=True)
    supervisors = SupervisorSerializer(read_only=True, many=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        ordering = ['-id']
        model = Topic
        fields = '__all__'

    def create(self,validated_data):
        fields = self.initial_data['fields']
        fieldsInstances = []
        
        for field in fields:
            fieldsInstances.append(Field.objects.get(id = field['id']))
        topic = Topic.objects.create(**validated_data)
        topic.fields.set(fieldsInstances)
        
        supervisors = self.initial_data['supervisors']
        supervisorsInstances = []
        
        for supervisor in supervisors:
            supervisorsInstances.append(User.objects.get(id = supervisor['id']))
        topic.supervisors.set(supervisorsInstances)

        return topic
    
    def update(self, instance, validated_data):
        fields = self.initial_data['fields']
        fieldsInstances = []

        for field in fields:
            fieldsInstances.append(Field.objects.get(pk = field['id']))
        instance.fields.set(fieldsInstances) 

        supervisors = self.initial_data['supervisors']
        supervisorsInstances = []
        for supervisor in supervisors:
            supervisorsInstances.append(User.objects.get(pk = supervisor['id']))
        instance.supervisors.set(supervisorsInstances) 

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

class TopicDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    fields = FieldSerializer(many=True)
    supervisors = SupervisorSerializer(many=True)
    topic_information = TopicInformationSerializer(read_only=True)
    
    class Meta:
        model = Topic
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    applicants = ApplicantsSerializer(read_only=True,many=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('created_on', 'updated_on', 'topic', 'user')

    def create(self,validated_data):
        topic = validated_data['topic']
        allowed_organization_ids = [str(org.id) for org in topic.course.allowed_organizations.all()]
        
        applicants_data = self.initial_data['applicants']
        if len(applicants_data) > 2:
            raise ValidationError("More than 2 applicants are not allowed.")

        applicantsInstances = []
        for applicant_data in applicants_data:
            applicant = User.objects.get(id=applicant_data['id'])
            applicant_group_names = [group.name for group in applicant.groups.all()]
            if not any(group_name in allowed_organization_ids for group_name in applicant_group_names):
                raise ValidationError(f"Applicant with ID {applicant.id} does not belong to an allowed organization.")
            applicantsInstances.append(applicant)
            
        application = Application.objects.create(**validated_data)
        application.applicants.set(applicantsInstances)

        return application

class ApplicationApprovalSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()
    class Meta:
        model = ApplicationApproval
        fields = '__all__'

class TopicRequestSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    fields = FieldSerializer(read_only=True,many=True)
    supervisors = SupervisorSerializer(read_only=True,many=True)
    creator = UserDetailSerializer(read_only=True)

    class Meta:
        ordering = ['-id']
        model = TopicRequest
        fields = '__all__'

    def create(self,validated_data):
        fields = self.initial_data['fields']
        fieldsInstances = []
        
        for field in fields:
            fieldsInstances.append(Field.objects.get(id = field['id']))
        topic_request = TopicRequest.objects.create(**validated_data)
        topic_request.fields.set(fieldsInstances)
        
        supervisors = self.initial_data['supervisors']
        supervisorsInstances = []
        
        for supervisor in supervisors:
            supervisorsInstances.append(User.objects.get(id = supervisor['id']))
        topic_request.supervisors.set(supervisorsInstances)

        return topic_request
    
    def update(self, instance, validated_data):
        fields = self.initial_data['fields']
        fieldsInstances = []

        for field in fields:
            fieldsInstances.append(Field.objects.get(pk = field['id']))
        instance.fields.set(fieldsInstances) 

        supervisors = self.initial_data['supervisors']
        supervisorsInstances = []
        for supervisor in supervisors:
            supervisorsInstances.append(User.objects.get(pk = supervisor['id']))
        instance.supervisors.set(supervisorsInstances) 

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

class TopicRequestApprovalSerializer(serializers.ModelSerializer):
    topic_request = TopicRequestSerializer()

    class Meta:
        model = TopicRequestApproval
        fields = '__all__'
        