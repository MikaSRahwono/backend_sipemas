from django.db import IntegrityError
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from api.permissions import IsManager, IsSecretary, IsSecretaryAndManager

from .models import *
from .serializers import *

from ..marketplace.serializers import FieldSerializer
from ..marketplace.models import Field

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsManager()]
        if self.action in ['information', 'activity_steps']:
            if self.request.method == 'GET':
                return []
            else:
                return [IsManager()]
        return []
    
    serializer_class = CourseSerializer
    model = Course
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = CourseSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save(kd_mk = request.data['kd_mk'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "Error occurred while creating the course"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super().destroy(self)
        return Response({'msg': 'Success delete course'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        course = self.get_object()

        existing_kd_mk = course.kd_mk
        request.data.setdefault('kd_mk', existing_kd_mk)

        serializer = CourseSerializer(course, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def information(self, request, pk=None):
        try:
            course = self.get_object()

            if request.method == 'GET':
                try:
                    course_information = CourseInformation.objects.get(course=course)
                    return render(request, "marketplace/topic_detail.html", {"html": course_information.__str__})
                except CourseInformation.DoesNotExist:
                    return Response({"error": "CourseInformation not found"}, status=status.HTTP_404_NOT_FOUND)
            
            elif request.method == 'POST':
                try:
                    serializer = CourseInformationSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(course=course)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError as e:
                        return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
            
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
        
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['GET', 'DELETE'], url_path='activity_steps', permission_classes = [IsAuthenticated])
    def activity_steps(self, request, pk=None):
        try:
            course = self.get_object()

            if request.method == 'GET':
                try:
                    activity_steps = ActivityStep.objects.filter(course=course).order_by('index')
                    serializer = ActivityStepSerializer(activity_steps, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except CourseInformation.DoesNotExist:
                    return Response({"error": "CourseInformation not found"}, status=status.HTTP_404_NOT_FOUND)
                
            if request.method == 'DELETE':
                try:
                    activity_steps = ActivityStep.objects.filter(course=course).order_by('index')
                    for step in activity_steps:
                        step.delete()
                    return Response({"success": "Activity Steps deleted"}, status=status.HTTP_200_OK)
                except ActivityStep.DoesNotExist:
                    return Response({"error": "ActivityStep not found"}, status=status.HTTP_404_NOT_FOUND)
            
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
class FieldViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'information']:
            return [IsManager()]
        return []
    
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

    def destroy(self, request, *args, **kwargs):
        super().destroy(self)
        return Response({'msg': 'Success delete field'}, status=status.HTTP_200_OK)

class ActivityStepViewSet(viewsets.ModelViewSet):
    queryset = ActivityStep.objects.all()
    serializer_class = ActivityStepSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            return [IsManager()]

    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_information', permission_classes=[IsAuthenticated])
    def step_information(self, request, pk=None):
        activity_step = ActivityStep.objects.get(pk = pk)

        if request.method == 'GET':
            try:
                step_information = StepInformation.objects.get(activity_step=activity_step)
                serializer = StepInformationSerializer(step_information)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except StepInformation.DoesNotExist:
                return Response({'error': 'Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if activity_step.type == "INF":
                    serializer = StepInformationSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(activity_step=activity_step)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be compatible with the step type'}, status=status.HTTP_400_BAD_REQUEST)
            except StepInformation.DoesNotExist:
                return Response({'error': 'Activity Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                step_information = StepInformation.objects.get(activity_step=activity_step)
                serializer = StepInformationSerializer(step_information, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except StepInformation.DoesNotExist:
                return Response({'error': 'Step Information does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_assignment', permission_classes=[IsAuthenticated])
    def step_assignment(self, request, pk=None):
        activity_step = ActivityStep.objects.get(pk = pk)

        if request.method == 'GET':
            try:
                step_assignment = StepAssignment.objects.get(activity_step=activity_step)
                serializer = StepAssignmentSerializer(step_assignment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except StepAssignment.DoesNotExist:
                return Response({'error': 'Assignment Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if activity_step.type == "ASG":
                    serializer = StepAssignmentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(activity_step=activity_step)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be compatible with the step type'}, status=status.HTTP_400_BAD_REQUEST)
            except StepAssignment.DoesNotExist:
                return Response({'error': 'Assignment Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                step_assignment = StepAssignment.objects.get(activity_step=activity_step)
                serializer = StepAssignmentSerializer(step_assignment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except StepAssignment.DoesNotExist:
                return Response({'error': 'Step Assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_sidang', permission_classes=[IsAuthenticated])
    def step_sidang(self, request, pk=None):
        activity_step = ActivityStep.objects.get(pk = pk)

        if request.method == 'GET':
            try:
                step_sidang = StepSidang.objects.get(activity_step=activity_step)
                serializer = StepSidangSerializer(step_sidang)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except StepSidang.DoesNotExist:
                return Response({'error': 'Sidang Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if activity_step.type == "SID":
                    serializer = StepSidangSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(activity_step=activity_step)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be compatible with the step type'}, status=status.HTTP_400_BAD_REQUEST)
            except StepSidang.DoesNotExist:
                return Response({'error': 'Sidang Step does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                step_sidang = StepSidang.objects.get(activity_step=activity_step)
                serializer = StepSidangSerializer(step_sidang, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except StepSidang.DoesNotExist:
                return Response({'error': 'Step Sidang does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'], url_path='step_components', permission_classes=[IsAuthenticated])
    def step_components(self, request, pk=None):
        activity_step = ActivityStep.objects.get(pk = pk)

        if request.method == 'GET':
            try:
                step_components = StepComponent.objects.filter(activity_step=activity_step)
                serializer = StepComponentSerializer(step_components, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except StepComponent.DoesNotExist:
                return Response({'error': 'Step Assignment Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if activity_step.type == "ASG":
                    serializer = StepComponentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(activity_step=activity_step)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be compatible Assignment type'}, status=status.HTTP_400_BAD_REQUEST)
            except StepComponent.DoesNotExist:
                return Response({'error': 'Step Assignment Component does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], url_path='step_components/(?P<index>\d+)', permission_classes=[IsAuthenticated])
    def manage_step_component(self, request, pk=None, index=None):
        activity_step = ActivityStep.objects.get(pk = pk)

        if request.method == 'DELETE':
            try:
                step_component = StepComponent.objects.get(activity_step=activity_step, index=index)
                step_component.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except StepComponent.DoesNotExist:
                return Response({'error': 'Step Assignment Component does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_components/(?P<index>\d+)/announcement_components', permission_classes=[IsAuthenticated])
    def announcement_component(self, request, pk=None, index=None):
        activity_step = ActivityStep.objects.get(pk = pk)
        step_component = StepComponent.objects.get(activity_step = activity_step, index=index)

        if request.method == 'GET':
            try:
                announcement_component = AnnouncementComponent.objects.get(step_component=step_component)
                serializer = AnnouncementComponentSerializer(announcement_component)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except AnnouncementComponent.DoesNotExist:
                return Response({'error': 'Announcement component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if step_component.type == "ANN":
                    serializer = AnnouncementComponentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(step_component=step_component)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be an announcement step'}, status=status.HTTP_400_BAD_REQUEST)
            except AnnouncementComponent.DoesNotExist:
                return Response({'error': 'Announcement Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                announcement_component = AnnouncementComponent.objects.get(step_component=step_component)
                serializer = AnnouncementComponentSerializer(announcement_component, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except AnnouncementComponent.DoesNotExist:
                return Response({'error': 'Announcement Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_components/(?P<index>\d+)/information_components', permission_classes=[IsAuthenticated])
    def information_component(self, request, pk=None, index=None):
        activity_step = ActivityStep.objects.get(pk = pk)
        step_component = StepComponent.objects.get(activity_step = activity_step, index=index)

        if request.method == 'GET':
            try:
                information_component = InformationComponent.objects.get(step_component=step_component)
                serializer = InformationComponentSerializer(information_component)
                return InformationComponent(serializer.data, status=status.HTTP_201_CREATED)
            except InformationComponent.DoesNotExist:
                return Response({'error': 'Information Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if step_component.type == "INF":
                    serializer = InformationComponentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(step_component=step_component)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be an information step'}, status=status.HTTP_400_BAD_REQUEST)
            except InformationComponent.DoesNotExist:
                return Response({'error': 'Information Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                information_component = InformationComponent.objects.get(step_component=step_component)
                serializer = InformationComponentSerializer(information_component, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except InformationComponent.DoesNotExist:
                return Response({'error': 'Information Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=True, methods=['GET', 'POST', 'PUT'], url_path='step_components/(?P<index>\d+)/assignment_components', permission_classes=[IsAuthenticated])
    def assignment_component(self, request, pk=None, index=None):
        activity_step = ActivityStep.objects.get(pk = pk)
        step_component = StepComponent.objects.get(activity_step = activity_step, index=index)

        if request.method == 'GET':
            try:
                assignment_component = AssignmentComponent.objects.get(step_component=step_component)
                serializer = AssignmentComponentSerializer(assignment_component)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except AssignmentComponent.DoesNotExist:
                return Response({'error': 'Assignment component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                if step_component.type == "ASG":
                    serializer = AssignmentComponentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(step_component=step_component)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Must be an announcement step'}, status=status.HTTP_400_BAD_REQUEST)
            except AssignmentComponent.DoesNotExist:
                return Response({'error': 'Assignment Component does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                assignment_component = AssignmentComponent.objects.get(step_component=step_component)
                serializer = AssignmentComponentSerializer(assignment_component, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except AssignmentComponent.DoesNotExist:
                return Response({'error': 'Assignment Component does not exist'}, status=status.HTTP_404_NOT_FOUND)