from rest_framework import serializers
from .models import *
from ..user.serializers import UserDetailSerializer, UserProfileSerializer
from ..course.serializers import CourseSerializer

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

class TopicListSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    fields = FieldSerializer(read_only=True,many=True)
    supervisors = SupervisorSerializer(read_only=True,many=True)

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
        try: 
            fields = self.initial_data['fields']
            fieldsInstances = []
            for field in fields:
                fieldsInstances.append(Field.objects.get(pk = field['id']))
            instance.fields.set(fieldsInstances) 

            supervisors = self.initial_data['supervisors']
            supervisorsInstances = []
            for supervisor in supervisors:
                supervisorsInstances.append(Field.objects.get(pk = supervisor['id']))
            instance.supervisors.set(supervisorsInstances) 

        except:
            pass
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

class ApplicationApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationApproval
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['praproposal', 'is_approved', 'created_on', 'updated_on']