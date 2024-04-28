from asyncio import mixins
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from api.academic.models import ActivityStep, AssignmentComponent
from api.activity.models import Activity, FileSubmission, LogSubmission
from api.activity.serializers import ActivitySerializer, FileSubmissionSerializer, LogSubmissionSerializer, StepCompletionSerializer

# Create your views here.
class ActivityViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    queryset = Activity.objects.all()

    def get_activity_and_component(self, pk, assignment_component_id):
        activity = get_object_or_404(Activity, pk=pk)
        assignment_component = get_object_or_404(AssignmentComponent, id=assignment_component_id)
        return activity, assignment_component
    
    def get_activity_and_activity_step(self, pk, activity_step_id):
        activity = get_object_or_404(Activity, pk=pk)
        activity_step = get_object_or_404(ActivityStep, id=activity_step_id)
        return activity, activity_step
    
    @action(detail=True, methods=['POST', 'PUT'], url_path='assignment_components/(?P<assignment_component_id>\d+)/log_submission', permission_classes=[IsAuthenticated])
    def log_submission(self, request, pk=None, assignment_component_id=None):
        activity, assignment_component = self.get_activity_and_component(pk, assignment_component_id)

        def handle_post_request(self, request, activity, assignment_component):
            if assignment_component.type != "LOG":
                return Response({'error': 'Must be compatible with the assignment type'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = LogSubmissionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(activity=activity, assignment_component=assignment_component)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def handle_put_request(self, request, activity, assignment_component):
            try:
                log_submission = LogSubmission.objects.get(activity=activity, assignment_component=assignment_component)
                serializer = LogSubmissionSerializer(log_submission, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except LogSubmission.DoesNotExist:
                return Response({'error': 'Log Submission does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        if request.method == 'POST':
            return handle_post_request(request, activity, assignment_component)
        elif request.method == 'PUT':
            return handle_put_request(request, activity, assignment_component)

    @action(detail=True, methods=['POST', 'PUT'], url_path='assignment_components/(?P<assignment_component_id>\d+)/file_submission', permission_classes=[IsAuthenticated])
    def file_submission(self, request, pk=None, assignment_component_id=None):
        activity, assignment_component = self.get_activity_and_component(pk, assignment_component_id)

        def handle_post_request(self, request, activity, assignment_component):
            if assignment_component.type != "SUB":
                return Response({'error': 'Must be compatible with the assignment type'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = FileSubmissionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(activity=activity, assignment_component=assignment_component)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def handle_put_request(self, request, activity, assignment_component):
            try:
                file_submission = FileSubmission.objects.get(activity=activity, assignment_component=assignment_component)
                serializer = FileSubmissionSerializer(file_submission, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FileSubmission.DoesNotExist:
                return Response({'error': 'File Submission does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        if request.method == 'POST':
            return handle_post_request(request, activity, assignment_component)
        elif request.method == 'PUT':
            return handle_put_request(request, activity, assignment_component)

    @action(detail=True, methods=['POST'], url_path='activity_step/(?P<activity_step_id>\d+)/complete', permission_classes=[IsAuthenticated])
    def complete_step(self, request, pk=None, activity_step_id=None):
        activity, activity_step = self.get_activity_and_activity_step(pk, activity_step_id)

        def handle_post_request(self, request, activity, activity_step):
            serializer = StepCompletionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(activity=activity, activity_step=activity_step, is_completed=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        if request.method == 'POST':
            return handle_post_request(request, activity, activity_step)
