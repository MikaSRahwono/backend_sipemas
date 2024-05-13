from django.shortcuts import render

from api.activity.models import Activity
from api.activity.serializers import ActivitySerializer
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

from django.db import IntegrityError
import django_filters

from api.marketplace.serializers import ApplicationApprovalSerializer, ApplicationSerializer, TopicListSerializer, TopicRequestApprovalSerializer, TopicRequestSerializer
from api.permissions import IsAdminOrIsSelf, IsAdmin, IsLecturer, IsSelf

from .models import *
from .serializers import *
from .filters import *

class UserPagination(PageNumberPagination):
    page_size = 20

class OrganizationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrganizationSerializer
    model = Organization
    queryset = Organization.objects.all()    

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
    model = User
    queryset = User.objects.all()
    filter_backends = [OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = (IsAuthenticated,)

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
        print(request.user.id)
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
    
    @action(detail=True, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAdmin])
    def profile(self, request, pk=None):
        user = self.get_object(pk = pk)

        if request.method == 'GET':
            try:
                user_profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(user_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save(user=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            try:
                user_profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(user_profile, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAdmin])
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
            user_detail = UserDetail.objects.get(user=user)
            serializer = UserDetailSerializer(user_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PATCH'], url_path='change_availability', permission_classes=[IsAdmin])
    def change_availability(self, request, pk=None):
        user = self.get_object(pk=pk)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_open = not user_profile.is_open
        user_profile.save()
        return Response({'message': 'Availability changed successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH', 'PUT'], url_path='update_picture', permission_classes=[IsAdmin])
    def update_picture(self, request, pk=None):
        user = self.get_object(pk=pk)
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    def get_object(self, pk):
        try:
            return User.objects.get(pk = pk)
        except:
            raise ValidationError({'msg':'User Does not exist'})
        
    serializer_class = UserSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.none()  
    pagination_class = None 

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)
    
    def update(self, request):
        user = self.request.user
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @action(detail=False, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                user_profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(user_profile, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            serializer = UserProfileSerializer(data=request.data, context={'request': self.request})
            if serializer.is_valid():
                try:
                    serializer.save(user=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            try:
                user_profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(user_profile, data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['GET', 'POST', 'PUT'], permission_classes=[IsAuthenticated])
    def information(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                user_detail = UserDetail.objects.get(user=user)
                serializer = UserDetailSerializer(user_detail, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except UserDetail.DoesNotExist:
                return Response({'error': 'User detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            try:
                serializer = UserDetailSerializer(data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save(user=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserDetail.DoesNotExist:
                return Response({'error': 'User detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                user_detail = UserDetail.objects.get(user=user)
                serializer = UserDetailSerializer(user_detail, data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserDetail.DoesNotExist:
                return Response({'error': 'User detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['PATCH'], url_path='change_availability', permission_classes=[IsAuthenticated])
    def change_availability(self, request):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_open = not user_profile.is_open
        user_profile.save()
        return Response({'message': 'Availability changed successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH', 'PUT'], url_path='update_picture', permission_classes=[IsAuthenticated])
    def update_picture(self, request):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data, context={'request': self.request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET', 'PUT'], url_path='applications', permission_classes=[IsAuthenticated])
    def applications(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                applications = Application.objects.filter(creator=user)
                serializer = ApplicationSerializer(applications, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Application.DoesNotExist:
                return Response({'error': 'Applications does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                application = Application.objects.get(creator=user)
                serializer = ApplicationSerializer(application, data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserDetail.DoesNotExist:
                return Response({'error': 'Applications does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET', 'PUT'], url_path='application_approvals', permission_classes=[IsAuthenticated])
    def application_approvals(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                approval = ApplicationApproval.objects.filter(approvee=user)
                serializer = ApplicationApprovalSerializer(approval, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Application.DoesNotExist:
                return Response({'error': 'Applications does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                approval = ApplicationApproval.objects.get(approvee=user)
                serializer = ApplicationApprovalSerializer(approval, data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except ApplicationApproval.DoesNotExist:
                return Response({'error': 'Applications does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET', 'PUT'], url_path='topic_requests', permission_classes=[IsAuthenticated])
    def topic_requests(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                topic_request = TopicRequest.objects.filter(user=user)
                serializer = TopicRequestSerializer(topic_request, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except TopicRequest.DoesNotExist:
                return Response({'error': 'TopicRequest does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                topic_request = TopicRequest.objects.get(user=user)
                serializer = TopicRequestSerializer(topic_request, data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except TopicRequest.DoesNotExist:
                return Response({'error': 'TopicRequest does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET', 'PUT'], url_path='topic_request_approvals', permission_classes=[IsAuthenticated])
    def topic_request_approvals(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                approval = TopicRequestApproval.objects.filter(approvee=user)
                serializer = TopicRequestApprovalSerializer(approval, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except TopicRequestApproval.DoesNotExist:
                return Response({'error': 'TopicRequestApproval does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PUT':
            try:
                approval = TopicRequestApproval.objects.get(approvee=user)
                serializer = TopicRequestApprovalSerializer(approval, data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except TopicRequestApproval.DoesNotExist:
                return Response({'error': 'TopicRequestApproval does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'], url_path='created-topics', permission_classes=[IsLecturer])
    def created_topics(self, request):
        user = self.request.user

        if request.method == 'GET':
            try:
                topic = Topic.objects.filter(creator=user)
                serializer = TopicListSerializer(topic, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Application.DoesNotExist:
                return Response({'error': 'Topic does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=False, methods=['GET'], url_path='topic-requests',  permission_classes=[IsAuthenticated])
    def topic_requests(self, request, pk=None):
        try:
            user = self.request.user
            
            if request.method == 'GET':
                try:
                    topic_requests = TopicRequest.objects.filter(creator=user)
                    serializer = TopicRequestSerializer(topic_requests, many=True, context={'request': self.request})
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except TopicRequest.DoesNotExist:
                    return Response({'error': 'Topic Request does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
        except IntegrityError as e:
            return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'], url_path='activities',  permission_classes=[IsAuthenticated])
    def activities(self, request, pk=None):
        try:
            user = self.request.user
            
            if request.method == 'GET':
                try:
                    activity = Activity.objects.filter(supervisees=user)
                    serializer = ActivitySerializer(activity, many=True, context={'request': self.request})
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Activity.DoesNotExist:
                    return Response({'error': 'Activities does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
        except IntegrityError as e:
            return Response({'error': 'Integrity Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'], url_path='roles')
    def roles(self, request, pk=None):
        # try:
            user = self.request.user

            serializer = GroupsSerializer(user)
            return Response(serializer.data)
    
        # except:
        #     return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

