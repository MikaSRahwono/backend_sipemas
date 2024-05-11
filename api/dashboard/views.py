from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User, Group

from api.academic.models import AssignmentComponent, Course
from api.academic.serializers import AssignmentComponentSerializer
from api.activity.models import Activity
from api.activity.serializers import ActivitySerializer
from api.dashboard.models import Note
from api.dashboard.serializers import NoteSerializer, StudentActivitySerializer
from api.permissions import IsSecretary
from api.user.serializers import UserSerializer
from api.user.models import User

# Create your views here.

class SecretaryDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    permission_classes = (IsSecretary, IsAuthenticated,)
    queryset = Activity.objects.all()  
    pagination_class = None 

    @action(detail=False, methods=['POST', 'GET'], url_path='notes/(?P<activity_id>\w+)')
    def notes(self, request, activity_id=None):
        # try:
            user = self.request.user
            
            user_group_names = [group.name for group in user.groups.all()]
            activities = super().get_queryset().filter(
                topic__course__allowed_organizations__id__in=user_group_names
            ).distinct()

            activity = activities.get(id=activity_id)
            if request.method == 'GET':
                try:
                    notes = Note.objects.filter(activity=activity)
                    serializer = NoteSerializer(notes, context={'request': self.request}, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Note.DoesNotExist:
                    return Response({'error': 'User detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            elif request.method == 'POST':
                try:
                    serializer = NoteSerializer(data=request.data, context={'request': self.request})
                    if serializer.is_valid():
                        serializer.save(creator=user, activity=activity)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Note.DoesNotExist:
                    return Response({'error': 'User detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
        # except:
        #     return Response({"error": "There's Something Wrong"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'], url_path='course_assignments/(?P<kd_mk>\w+)')
    def course_assignments(self, request, kd_mk=None):
        try:
            user = self.request.user
            assignment_components = AssignmentComponent.objects.filter(
                step_component__activity_step__course__kd_mk=kd_mk
            ).distinct()

            serializer = AssignmentComponentSerializer(assignment_components, context={'request': self.request}, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'], url_path='student_activities')
    def student_activities(self, request, pk=None):
        try:
            user = self.request.user
            
            user_group_names = [group.name for group in user.groups.all()]
            activities = super().get_queryset().filter(
                topic__course__allowed_organizations__id__in=user_group_names
            ).distinct()

            serializer = StudentActivitySerializer(activities, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['GET'], url_path='student_no_activity/(?P<kd_mk>\w+)')
    def student_no_activity(self, request, kd_mk=None):
        try:
            user = self.request.user
            group = Group.objects.get(name='Student')
            students = User.objects.filter(groups=group)
            course = Course.objects.get(kd_mk=kd_mk)

            user_group_names = [group.name for group in user.groups.all()]
            students_per_organizations = students.filter(
                groups__name__in=user_group_names
            ).distinct()

            student_no_activity_data = []

            for student in students_per_organizations:
                if not Activity.objects.filter(supervisees=student, course=course).exists():
                    student_no_activity_data.append(student)
            
            serializer = UserSerializer(student_no_activity_data, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_404_NOT_FOUND)