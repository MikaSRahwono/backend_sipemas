from django.db import models

from api.activity.storage import FileStorage
from api.user.models import User
from api.academic.models import ActivityStep, AssignmentComponent, Course
from api.marketplace.models import Topic, Application, TopicRequest

class Activity(models.Model):        
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.DO_NOTHING, null=True, blank=True)
    topic_request = models.OneToOneField(TopicRequest, on_delete=models.DO_NOTHING, null=True, blank=True)
    supervisees = models.ManyToManyField(User, related_name='supervisee')
    supervisors = models.ManyToManyField(User, related_name='supervisors')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class LogSubmission(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='logsubmissions')
    assignment_component = models.ForeignKey(AssignmentComponent, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class FileSubmission(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='filesubmissions')
    assignment_component = models.OneToOneField(AssignmentComponent, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='assignments/', null=False, blank=False, storage=FileStorage(), max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class StepCompletion(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='stepcompletions')
    activity_step = models.ForeignKey(ActivityStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)