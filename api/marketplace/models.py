from django.db import models
from django.utils.translation import gettext_lazy as _
from api.user.models import Field
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

from ..academic.models import Course

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    is_open = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_creator')
    num_of_people = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(Field)
    supervisors = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class TopicInformation(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    html = RichTextField()

    def __str__(self):
        return self.html

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicants_leader')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(User, related_name='applicants')
    praproposal = models.CharField(max_length=256)
    is_approved = models.BooleanField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class ApplicationApproval(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    approvee = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True)
    is_supervisor = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)

class TopicRequest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_request_creator')
    num_of_people = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(Field)
    supervisors = models.ManyToManyField(User, related_name='topic_request_supervisors')
    applicants = models.ManyToManyField(User, related_name='topic_request_applicants')
    description = models.TextField(null=True)
    is_approved = models.BooleanField(null=True)

class TopicRequestApproval(models.Model):
    topic_request = models.ForeignKey(TopicRequest, on_delete=models.CASCADE)
    approvee = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True)
    is_supervisor = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)
    

