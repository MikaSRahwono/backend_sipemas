from django.db import IntegrityError
from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from api.activity.models import Activity
from api.permissions import IsManager, IsSecretary, IsLecturer

from .signals import application_approved_signal, topic_request_approved_signal, create_application_approval_signal, create_request_approval_signal

import django_filters

from .models import *
from .serializers import *
from .filters import *


class TopicPagination(PageNumberPagination):
    page_size = 10

class TopicViewSet(viewsets.ModelViewSet):

    serializer_class = TopicListSerializer
    pagination_class = TopicPagination
    model = Topic
    queryset = Topic.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TopicFilter
    ordering_fields = ['title', 'created_on'] 

    def get_serializer_class(self):
        if self.action == 'list':
            return TopicListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return TopicDetailSerializer
        else:
            return super().get_serializer_class()
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsLecturer()]
        elif self.action in ['apply', 'request']:
            return [IsAuthenticated()]
        elif self.action in ['all_requests']:
            return [IsLecturer(), IsSecretary()]
        elif self.action in ['information']:
            if self.request.method == 'GET':
                return []
            else:
                return [IsLecturer()]
        return []
    
    def get_object(self, pk):
        try:
            return Topic.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'Topic Does not exist'})

    def retrieve(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicDetailSerializer(topic, context={'request': self.request})
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        user = self.request.user
        topic = self.get_object(pk)
        if topic.creator != user:
            return Response({"error": f"{user.email} doesn't hane permission to delete topics created by {topic.creator.email}"}, status=status.HTTP_400_BAD_REQUEST)
        topic.delete()
        return Response({"success": "Topic deleted"}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        user = self.request.user

        serializer = TopicListSerializer(data = request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk):
        user = self.request.user
        topic = self.get_object(pk = pk)

        if topic.creator != user:
            return Response({"error": "You don't have permission to change this topic"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TopicListSerializer(topic, data = request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def information(self, request, pk=None):
        try:
            topic = self.get_object(pk=pk)

            if request.method == 'GET':
                try:
                    topic_information = TopicInformation.objects.get(topic=topic)
                    return render(request, "marketplace/topic_detail.html", {"html": topic_information.__str__})
                except TopicInformation.DoesNotExist:
                        return Response({"error": "TopicInformation not found"}, status=status.HTTP_404_NOT_FOUND)
            
            elif request.method == 'POST':
                try:
                    user = self.request.user
                    if topic.creator != user:
                        return Response({"error": "You don't have permission to change this topic"}, status=status.HTTP_404_NOT_FOUND)
        
                    serializer = TopicInformationSerializer(data=request.data, context={'request': self.request})
                    if serializer.is_valid():
                        serializer.save(topic=topic)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError as e:
                    return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
            
            elif request.method == 'PUT':
                try:
                    user = self.request.user
                    if topic.creator != user:
                        return Response({"error": "You don't have permission to change this topic"}, status=status.HTTP_404_NOT_FOUND)
        
                    topic_information = TopicInformation.objects.get(topic=topic)
                    serializer = TopicInformationSerializer(topic_information, data=request.data, context={'request': self.request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except TopicInformation.DoesNotExist:
                    return Response({"error": "Topic information not found"}, status=status.HTTP_404_NOT_FOUND)
                
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['POST'], url_path='apply')
    def apply(self, request, pk=None):
        try:
            topic = self.get_object(pk=pk)
            user = self.request.user
            
            allowed_organization_ids = [str(org.id) for org in topic.course.allowed_organizations.all()]
            user_group_names = [group.name for group in user.groups.all()]

            if not any(group_name in allowed_organization_ids for group_name in user_group_names):
                return Response({"error": "Your study program are allowed for this topic"}, status=status.HTTP_403_FORBIDDEN)

            user_activities = Activity.objects.filter(supervisees=user)
            if topic.course.course_type == "OO":
                for activity in user_activities:
                    if activity.is_completed is None:
                        return Response({'error': f"You already have other running activity in course {activity.topic.course.nm_mk}"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = ApplicationSerializer(data=request.data, context={'request': request, 'topic': topic})
            if serializer.is_valid():
                application = serializer.save(topic=topic, creator=user)
                create_application_approval_signal.send(sender=Application, instance=application, action='post_add')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['POST'], url_path='request')
    def request(self, request, pk=None):
            try:
                user = self.request.user
                
                serializer = TopicRequestSerializer(data=request.data, context={'request': self.request})

                course = Course.objects.get(kd_mk=request.data['course'])

                allowed_organization_ids = [str(org.id) for org in course.allowed_organizations.all()]
                user_group_names = [group.name for group in user.groups.all()]

                if not any(group_name in allowed_organization_ids for group_name in user_group_names):
                    return Response({"error": "Your study program are allowed for this topic"}, status=status.HTTP_403_FORBIDDEN)
                
                user_activities = Activity.objects.filter(supervisees=user)
                if course.course_type == "OO":
                    for activity in user_activities:
                        if activity.is_completed is None:
                            return Response({'error': f"You already have other running activity in course {activity.topic.course.nm_mk}"}, status=status.HTTP_403_FORBIDDEN)
                    
                if serializer.is_valid():
                    topic_request = serializer.save(creator=user)
                    create_request_approval_signal.send(sender=TopicRequest, instance=topic_request, action='post_add')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            except IntegrityError as e:
                return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=False, methods=['GET'], url_path='all-topic-requests')
    def all_requests(self, request, pk=None):
        try:
            user = self.request.user
            topic_requests = TopicRequest.objects.all()
            serializer = TopicRequestSerializer(topic_requests, many=True, context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except TopicRequest.DoesNotExist:
            return Response({'error': 'Topic Request does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
    
class ApplicationsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSecretary,)
    serializer_class = ApplicationSerializer
    model = Application
    queryset = Application.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ApplicationFilter
    ordering_fields = ['created_on']

    def get_queryset(self):
        topics_id = self.kwargs.get('topics_pk')
        if topics_id:
            return Application.objects.filter(topic__id=topics_id)
        return super().get_queryset()

    def retrieve(self, serializer):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class ApplicationApprovalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSecretary,)
    serializer_class = ApplicationApprovalSerializer
    model = ApplicationApproval
    queryset = ApplicationApproval.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['created_on']

    def retrieve(self, serializer):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self, pk):
        try:
            return ApplicationApproval.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'Application Approval Does not exist'})

    @action(detail=True, methods=['PATCH'], url_path='approve', permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        application_approval = self.get_object(pk)
        user = request.user

        user_activities = Activity.objects.filter(supervisees=user)
        for activity in user_activities:
            if activity.is_completed is None:
                return Response({'error': "You already have other running activity in course" + activity.topic.course.nm_mk}, status=status.HTTP_403_FORBIDDEN)

        if application_approval.approvee != user:
            return Response({'error': "You don't have permission to approve"}, status=status.HTTP_403_FORBIDDEN)

        if application_approval.is_approved:
            return Response({'message': 'Application already approved'}, status=status.HTTP_200_OK)

        application_approval.is_approved = True
        application_approval.approval_status = 1
        application_approval.save()

        application_approved_signal.send(sender=ApplicationApproval, application_approval=application_approval, user=user)
        
        return Response({'message': 'Application Approved'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['PATCH'], url_path='decline', permission_classes=[IsAuthenticated])
    def decline(self, request, pk=None):
        application_approval = self.get_object(pk)
        application = Application.objects.get(id=application_approval.application.id)
        user = request.user

        if application_approval.approvee != user:
            return Response({'error': "You don't have permission to decline"}, status=status.HTTP_403_FORBIDDEN)

        if application_approval.is_approved:
            return Response({'message': 'Application already declined'}, status=status.HTTP_200_OK)

        application_approval.is_approved = False
        application_approval.approval_status = -1
        all_application_approvals = ApplicationApproval.objects.filter(application=application_approval.application)

        for approval in all_application_approvals:
            approval.approval_status = -1

        application.is_approved = False
        application_approval.save()
        application.save()
        
        return Response({'message': 'Application Declined'}, status=status.HTTP_200_OK)
        
class TopicRequestViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSecretary,)
    serializer_class = TopicRequestSerializer
    model = TopicRequest
    queryset = TopicRequest.objects.all()
    ordering_fields = ['created_on']

    def get_queryset(self):
        topics_id = self.kwargs.get('topics_pk')
        if topics_id:
            return Application.objects.filter(topic__id=topics_id)
        return super().get_queryset()

    def retrieve(self, serializer):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

class TopicRequestApprovalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSecretary,)
    serializer_class = TopicRequestApprovalSerializer
    model = TopicRequestApproval
    queryset = TopicRequestApproval.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['created_on']

    def retrieve(self, serializer):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self, pk):
        try:
            return TopicRequestApproval.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'Topic Request Approval Does not exist'})

    @action(detail=True, methods=['PATCH'], url_path='approve', permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        topic_approval = self.get_object(pk)
        user = request.user

        user_activities = Activity.objects.filter(supervisees=user)
        for activity in user_activities:
            if activity.is_completed is None:
                return Response({'error': f"You already have other running activity in course {activity.topic.course.nm_mk}"}, status=status.HTTP_403_FORBIDDEN)

        if topic_approval.approvee != user:
            return Response({'error': "You don't have permission to approve"}, status=status.HTTP_403_FORBIDDEN)

        if topic_approval.is_approved:
            return Response({'message': 'Topic Request already approved'}, status=status.HTTP_200_OK)

        topic_approval.is_approved = True
        topic_approval.approval_status = 1
        topic_approval.save()

        topic_request_approved_signal.send(sender=TopicRequestApproval, topic_request_approval=topic_approval, user=user)
        
        return Response({'message': 'Topic Request Approved'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['PATCH'], url_path='decline', permission_classes=[IsAuthenticated])
    def decline(self, request, pk=None):
        topic_approval = self.get_object(pk)
        topic_request = TopicRequest.objects.get(id=topic_approval.topic_request.id)
        user = request.user

        if topic_approval.approvee != user:
            return Response({'error': "You don't have permission to decline"}, status=status.HTTP_403_FORBIDDEN)

        if topic_approval.is_approved:
            return Response({'message': 'Topic Request already declined'}, status=status.HTTP_200_OK)

        topic_approval.is_approved = False
        topic_approval.approval_status = -1
        all_topic_approvals = TopicRequestApproval.objects.filter(topic_request=topic_approval.topic_request)

        for approval in all_topic_approvals:
            approval.approval_status = -1

        topic_request.is_approved = False
        topic_approval.save()
        topic_request.save()
        
        return Response({'message': 'Topic Request Declined'}, status=status.HTTP_200_OK)