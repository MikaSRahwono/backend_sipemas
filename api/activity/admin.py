from django.contrib import admin

# Register your models here.
from .models import *

admin.register(
    Activity,
    ActivityStep,
    StepCompletion,
    LogSubmission,
    FileSubmission
    )(admin.ModelAdmin)