from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.db.models import Q


from api.academic.models import AssignmentComponent, Course
from api.academic.serializers import AssignmentComponentSerializer, CourseSerializer
from api.activity.models import Activity
from api.activity.serializers import ActivitySerializer
from api.dashboard.filters import ActivityFilter
from api.dashboard.models import Note
from api.dashboard.serializers import LecturerDataSerializer, NoteSerializer, StudentActivitySerializer, StudentDataSerializer, UserGroupsSerializer
from api.marketplace.models import Application, ApplicationApproval, Topic, TopicRequestApproval
from api.marketplace.serializers import ApplicationApprovalSerializer, TopicListSerializer, TopicRequestApprovalSerializer
from api.permissions import IsManager, IsLecturer, IsNotStudent, IsSecretary, IsSecretaryAndLecturer, IsSecretaryAndManager
from api.user.serializers import UserSerializer
from api.user.models import Organization, User

# Create your views here.

class SecretaryDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    permission_classes = (IsSecretaryAndManager, IsAuthenticated,)
    queryset = Activity.objects.all()  
    pagination_class = None 
    filterset_class = ActivityFilter

    @action(detail=False, methods=['GET'], url_path='overview')
    def overview(self, request, pk=None):
        try:
            user = self.request.user
            
            user_group_names = [group.name for group in user.groups.all()]
            students = User.objects.filter(
                groups__name="Student"
            ).distinct()
            students = students.filter(
                groups__name__in=user_group_names
            )

            students_have_activities = 0
            student_have_pending_approval = 0
            for student in students:
                if Activity.objects.filter(supervisees=student, is_completed=None).exists():
                    students_have_activities += 1
                elif ApplicationApproval.objects.filter(
                        Q(approvee=student) &
                        (Q(approval_status=0) | Q(approval_status=1))
                    ).exists() or TopicRequestApproval.objects.filter(
                        Q(approvee=student) &
                        (Q(approval_status=0) | Q(approval_status=1))
                    ).exists():
                    student_have_pending_approval += 1

            data = {
                'total_students': len(students),
                'students_have_activities': students_have_activities,
                'student_have_pending_approval': student_have_pending_approval
            }

            return Response(data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['POST', 'GET'], url_path='notes/(?P<activity_id>\w+)')
    def notes(self, request, activity_id=None):
        try:
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
                
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='student_no_activity/(?P<kd_mk>\w+)')
    def student_no_activity(self, request, kd_mk=None):
        try:
            user = self.request.user
            group = Group.objects.get(name='Student')
            students = User.objects.filter(groups=group)
            course = Course.objects.get(kd_mk=kd_mk)

            allowed_organizations = course.allowed_organizations.all()

            user_group_names = [group.name for group in Group.objects.filter(name__in=allowed_organizations)]
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
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='lecturers')
    def lecturer(self, request, pk=None):
        try:
            user = self.request.user
            
            lecturers = User.objects.filter(
                groups__name="Lecturer"
            ).distinct()

            serializer = LecturerDataSerializer(lecturers, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='lecturers/(?P<user_id>\d+)')
    def lecturer_profile(self, request, user_id=None):
        try:
            user = self.request.user

            serializer = LecturerDataSerializer(user, context={'request': self.request})
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LecturerDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    queryset = Activity.objects.all()  
    pagination_class = None 
    filterset_class = ActivityFilter
    permission_classes = (IsNotStudent, IsAuthenticated,)

    @action(detail=False, methods=['GET'], url_path='overview')
    def overview(self, request, pk=None):
        try:
            user = self.request.user

            serializer = LecturerDataSerializer(user, context={'request': self.request})
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['GET'], url_path='supervised_activities')
    def supervised_activities(self, request, pk=None):
        try:
            user = self.request.user
            
            activities = super().get_queryset().filter(supervisors=user)

            serializer = StudentActivitySerializer(activities, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='supervised_topics')
    def supervised_topics(self, request, pk=None):
        try:
            user = self.request.user
            
            topics = Topic.objects.filter(supervisors=user)

            serializer = TopicListSerializer(topics, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='application_approvals/(?P<topic_id>\d+)')
    def application_approvals(self, request, topic_id=None):
        try:
            user = self.request.user
            
            topic = Topic.objects.get(id=topic_id)
            application_approvals = ApplicationApproval.objects.filter(application__topic=topic, approvee=user)

            serializer = ApplicationApprovalSerializer(application_approvals, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['GET'], url_path='topic_request_approvals')
    def topic_request_approvals(self, request):
        try:
            user = self.request.user
            
            topic_request_approvals = TopicRequestApproval.objects.filter(topic_request__supervisors=user, approvee=user)

            serializer = TopicRequestApprovalSerializer(topic_request_approvals, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
           
    @action(detail=False, methods=['GET'], url_path='students')
    def students(self, request, pk=None):
        students = User.objects.filter(
            groups__name="Student"
        ).distinct()

        serializer = UserSerializer(students, context={'request': self.request}, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['GET'], url_path='students/(?P<student_id>\d+)')
    def student_profile(self, request, student_id=None):
        student = User.objects.get(id=student_id)

        serializer = StudentDataSerializer(student, context={'request': self.request})
        return Response(serializer.data)
        
        
class ManagerDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    queryset = Activity.objects.all()  
    pagination_class = None 
    filterset_class = ActivityFilter

    def get_permissions(self):
        if self.action in ['lecturer']:
            return [IsNotStudent()]
        return [IsManager()]


    @action(detail=False, methods=['GET'], url_path='overview')
    def overview(self, request, pk=None):
        try:
            user = self.request.user
            
            students = User.objects.filter(
                groups__name="Student"
            ).distinct()

            students_have_activities = 0
            student_have_pending_approval = 0
            for student in students:
                if Activity.objects.filter(supervisees=student, is_completed=None).exists():
                    students_have_activities += 1
                elif ApplicationApproval.objects.filter(
                        Q(approvee=student) &
                        (Q(approval_status=0) | Q(approval_status=1))
                    ).exists() or TopicRequestApproval.objects.filter(
                        Q(approvee=student) &
                        (Q(approval_status=0) | Q(approval_status=1))
                    ).exists():
                    student_have_pending_approval += 1

            data = {
                'total_students': len(students),
                'students_have_activities': students_have_activities,
                'student_have_pending_approval': student_have_pending_approval
            }

            return Response(data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['GET'], url_path='lecturers')
    def lecturer(self, request, pk=None):
        try:
            user = self.request.user
            
            lecturers = User.objects.filter(
                groups__name="Lecturer"
            ).distinct()

            serializer = LecturerDataSerializer(lecturers, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='user_roles')
    def user_roles(self, request, pk=None):
        try:
            user = self.request.user
            
            lecturers_and_secretaries = User.objects.filter(
                Q(groups__name="Lecturer") | Q(groups__name="Secretary")
            ).distinct()

            serializer = UserGroupsSerializer(lecturers_and_secretaries, context={'request': self.request}, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['POST', 'PUT'], url_path='user_roles/(?P<user_id>\d+)/add')
    def add_user_roles(self, request, user_id=None):
        try:            
            user = User.objects.get(id=user_id)

            group_names = request.data.get('group_names')

            if not group_names:
                return Response({"error": "group_name is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

            user.groups.clear()
            for group_name in group_names:
                group = Group.objects.get(name=group_name['id'])
                user.groups.add(group)

            serializer = UserGroupsSerializer(user, context={'request': self.request})
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)