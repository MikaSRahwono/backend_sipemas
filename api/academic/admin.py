from django.contrib import admin
from .models import *

admin.register(
    CourseInformation,
    Prerequisite,
    StepInformation,
    StepSidang,
    StepAssignment,
    StepComponent,
    InformationComponent,
    AnnouncementComponent,
    AssignmentComponent,
    )(admin.ModelAdmin)