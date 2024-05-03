from django.contrib import admin

# Register your models here.
from .models import *

admin.register(
    Course, 
    Topic,
    Field,
    TopicInformation,
    Application,
    ApplicationApproval,
    TopicRequest,
    TopicRequestApproval,
    )(admin.ModelAdmin)