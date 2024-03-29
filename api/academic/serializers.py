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
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('kd_mk',)
