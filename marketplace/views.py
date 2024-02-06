from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from rest_framework import viewsets

from .models import *
from .serializers import *

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = CourseSerializer
    model = Course
    queryset = Course.objects.all()

    def retrieve(self, serializer):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicListSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return TopicListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return TopicDetailSerializer
        else:
            return super().get_serializer_class()
        
    authentication_classes = []
    model = Topic
    queryset = Topic.objects.all()

    def retrieve(self,request, *args, **kwargs):
        instance = self.get_object()
        detailSerializer = TopicDetailSerializer(instance)
        return Response(detailSerializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class TopicInformationView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TopicInformationSerializer()
    queryset = TopicInformation.objects.all()
    def retrieve(self,request, *args, **kwargs):
        instance = self.get_object()
        detailSerializer = TopicInformationSerializer(instance)
        return render(request, 'marketplace/topic_detail.html', {'html': detailSerializer.data.get('html')})
    
class CourseInformationView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseInformationSerializer()
    queryset = CourseInformation.objects.all()
    def retrieve(self,request, *args, **kwargs):
        instance = self.get_object()
        detailSerializer = CourseInformationSerializer(instance)
        return render(request, 'marketplace/topic_detail.html', {'html': detailSerializer.data.get('html')})