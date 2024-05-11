from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.db.models import Q


from api.academic.models import AssignmentComponent, Course
from api.academic.serializers import AssignmentComponentSerializer
from api.activity.models import Activity
from api.activity.serializers import ActivitySerializer
from api.dashboard.filters import ActivityFilter
from api.dashboard.models import Note
from api.dashboard.serializers import LecturerDataSerializer, NoteSerializer, StudentActivitySerializer, StudentDataSerializer
from api.marketplace.models import Application, ApplicationApproval, Topic, TopicRequestApproval
from api.marketplace.serializers import ApplicationApprovalSerializer, TopicListSerializer, TopicRequestApprovalSerializer
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
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='lecturers')
    def lecturer(self, request, pk=None):
        try:
            user = self.request.user
            
            lecturers = User.objects.filter(
                groups__name="Lecturer"
            ).distinct()

            serializer = LecturerDataSerializer(lecturers, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LecturerDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = ActivitySerializer
    model = Activity
    permission_classes = (IsSecretary, IsAuthenticated,)
    queryset = Activity.objects.all()  
    pagination_class = None 
    filterset_class = ActivityFilter

    @action(detail=False, methods=['GET'], url_path='overview')
    def overview(self, request, pk=None):
        try:
            user = self.request.user

            serializer = LecturerDataSerializer(user)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['GET'], url_path='supervised_activities')
    def supervised_activities(self, request, pk=None):
        try:
            user = self.request.user
            
            activities = super().get_queryset().filter(supervisors=user)

            print(activities)

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
        try:
            user = self.request.user
            
            user_group_names = [group.name for group in user.groups.all()]
            students = User.objects.filter(
                groups__name="Student"
            ).distinct()
            students = students.filter(
                groups__name__in=user_group_names
            )

            serializer = UserSerializer(students, many=True)
            return Response(serializer.data)
    
        except:
            return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['GET'], url_path='students/(?P<student_id>\d+)')
    def student_profile(self, request, student_id=None):
        # try:
            user = self.request.user
            
            student = User.objects.get(id=student_id)

            serializer = StudentDataSerializer(student)
            return Response(serializer.data)
    
        # except:
        #     return Response({"error": "There's Something Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        