from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
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
        fields = '__all__'

class TopicListSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    fields = FieldSerializer(many=True)
    supervisors = UserSerializer(many=True)

    class Meta:
        model = Topic
        fields = '__all__'

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