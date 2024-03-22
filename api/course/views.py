from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import *
from .serializers import *

from ..marketplace.serializers import FieldSerializer
from ..marketplace.models import Field

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = CourseSerializer
    model = Course
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def information(self, request, pk=None):
        course = self.get_object()

        if request.method == 'GET':
            course_information = CourseInformation.objects.get(course=course)
            return render(request, "marketplace/topic_detail.html", {"html": course_information.__str__})

        
        elif request.method == 'POST':
            serializer = CourseInformationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(course=course)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            try:
                course_information = CourseInformation.objects.get(course=course)
                serializer = CourseInformationSerializer(course_information, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CourseInformation.DoesNotExist:
                return Response({"error": "Course information not found"}, status=status.HTTP_404_NOT_FOUND)

class FieldViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = FieldSerializer
    model = Field
    queryset = Field.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
