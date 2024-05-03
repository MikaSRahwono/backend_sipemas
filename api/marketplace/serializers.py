from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from ..user.serializers import UserDetailSerializer, UserProfileSerializer
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
    fields = FieldSerializer(read_only=True,many=True)
    supervisors = SupervisorSerializer(read_only=True,many=True)
    creator = UserDetailSerializer(read_only=True)

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
        applicants = self.initial_data['applicants']
        applicantsInstances = []

        if len(applicants) > 2:
            raise ValidationError("More than 3 applicants are not allowed.")
        
        for applicant in applicants:
            applicantsInstances.append(User.objects.get(id = applicant['id']))
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
        