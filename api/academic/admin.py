from django.contrib import admin
from .models import *

admin.register(
    CourseInformation,
    Course,
    Prerequisite,
    ActivityStep,
    StepInformation,
    StepSidang,
    StepAssignment,
    StepComponent,
    InformationComponent,
    AnnouncementComponent,
    AssignmentComponent
    )