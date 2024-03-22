from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

from ..academy.models import Course

class Field(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    is_open = models.BooleanField(default=True)
    num_of_people = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(Field)
    supervisors = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class TopicInformation(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    html = RichTextField()

    def __str__(self):
        return self.html

class Application(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    praproposal = models.CharField(max_length=256)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class ApplicationApproval(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    approvee = models.ManyToManyField(User)
    is_approved = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, auto_now=False, null=True)
    

