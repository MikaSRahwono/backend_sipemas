from django.contrib import admin

# Register your models here.
from .models import *

admin.register(Course, Topic, Field, TopicInformation, User, CourseInformation, Prerequisite)(admin.ModelAdmin)