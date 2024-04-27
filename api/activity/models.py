from django.db import models

from api.activity.storage import FileStorage
from api.user.models import User
from api.academic.models import AssignmentComponent, Course
from api.marketplace.models import Topic, Application

class Activity(models.Model):        
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.DO_NOTHING)
    supervisee = models.ManyToManyField(User, related_name='supervisee')
    supervisor = models.ManyToManyField(User, related_name='supervisor')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class LogSubmission(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    assignment_component = models.ForeignKey(AssignmentComponent, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class AssignmentSubmission(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    assignment_component = models.ForeignKey(AssignmentComponent, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256)
    body = models.TextField()
    file = models.FileField(upload_to='assignments/', null=False, blank=False, storage=FileStorage())
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class StepCompletion(models.Model):        
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    step_index = models.CharField(max_length=256)
    is_completed = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)