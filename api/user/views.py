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

import django_filters

from .models import *
from .serializers import *
from .filters import *

class UserPagination(PageNumberPagination):
    page_size = 20

class UsersViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        elif self.action in ['retrieve', 'update']:
            return UserSerializer
        else:
            return super().get_serializer_class()

    serializer_class = UserSerializer
    pagination_class = UserPagination
    authentication_classes = []
    model = User
    queryset = User.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = UserFilter

    def get_object(self, pk):
        try:
            return User.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'User Does not exist'})

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, pk=None):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, pk=None):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, pk=None):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk):
        user = self.get_object(pk = pk)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def profile(self, request, pk=None):
        user = self.get_object(pk=pk)

        if request.method == 'GET':
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif request.method == 'POST':
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    def information(self, request, pk=None):
        user = self.get_object(pk=pk)
        
        if request.method == 'GET':
            user_detail = UserDetail.objects.get(user=user)
            serializer = UserDetailSerializer(user_detail)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif request.method == 'POST':
            serializer = UserDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            serializer = UserDetailSerializer(user_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        