from django.contrib import admin
from .models import Course, CourseInformation, Prerequisite

admin.register(
    CourseInformation,
    Course,
    Prerequisite,)