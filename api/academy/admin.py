from django.contrib import admin
from .models import CourseInformation, Prerequisite

admin.register(
    CourseInformation,
    Prerequisite,)