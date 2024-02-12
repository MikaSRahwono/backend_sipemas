from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'

class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'

class CourseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInformation
        fields = ['html']

class CourseSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisiteSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
    
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class TopicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicInformation
        fields = ['html']

class TopicListSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    fields = FieldSerializer(read_only=True,many=True)
    supervisors = UserSerializer(read_only=True,many=True)

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
        topic = Topic.objects.create(**validated_data)
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
    supervisors = UserSerializer(many=True)
    topic_information = TopicInformationSerializer(read_only=True)
    
    class Meta:
        model = Topic
        fields = '__all__'

class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'

class ApplicationApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationApproval
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    application_approval = ApplicationApprovalSerializer(many=True, read_only=True)
    class Meta:
        model = Application
        fields = '__all__'