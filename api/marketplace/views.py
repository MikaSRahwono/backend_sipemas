from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from api.permissions import IsAdmin, ReadOnlyOrAdmin, IsLecturer

from .signals import application_creation_done

import django_filters

from .models import *
from .serializers import *
from .filters import *


class TopicPagination(PageNumberPagination):
    page_size = 10

class TopicViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return TopicListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return TopicDetailSerializer
        else:
            return super().get_serializer_class()
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'information']:
            if self.request.method == 'GET':
                return [ReadOnlyOrAdmin()]
            else:
                return [IsLecturer()]
        return []
    
    def get_object(self, pk):
        try:
            return Topic.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'Topic Does not exist'})
    
    serializer_class = TopicListSerializer
    pagination_class = TopicPagination
    model = Topic
    queryset = Topic.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TopicFilter
    ordering_fields = ['title', 'created_on'] 

    def retrieve(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicDetailSerializer(topic)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = TopicListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk):
        topic = self.get_object(pk = pk)
        serializer = TopicListSerializer(topic, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def information(self, request, pk=None):
        topic = self.get_object()

        if request.method == 'GET':
            topic_information = TopicInformation.objects.get(topic=topic)
            return render(request, "marketplace/topic_detail.html", {"html": topic_information.__str__})
        
        elif request.method == 'POST':
            serializer = TopicInformationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(topic=topic)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            serializer = TopicInformationSerializer(topic_information, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['POST'], url_path='apply')
    def apply(self, request, pk=None):
        topic = self.get_object(pk=pk)
        
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(topic = topic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApplicationViewSet(viewsets.ModelViewSet):
    authentication_classes = []
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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, request, *args, **kwargs):
        application_data = request.data.copy()
        users_data = application_data.pop('users', [])

        serializer = self.get_serializer(data=application_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        application = Application.objects.filter(topic__id=application_data.pop('id'))

        application_creation_done.send(sender=Application, users_data_list=users_data, application=application)


    def perform_update(self, serializer):
        serializer.save()