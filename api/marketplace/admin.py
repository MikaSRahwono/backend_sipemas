from django.contrib import admin

# Register your models here.
from .models import *

admin.register(
    Course, 
    Topic,
    Field,
    TopicInformation,
    CourseInformation,
    Prerequisite,
    Application,
    ApplicationApproval)(admin.ModelAdmin)