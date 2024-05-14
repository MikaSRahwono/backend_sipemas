from django.contrib import admin


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