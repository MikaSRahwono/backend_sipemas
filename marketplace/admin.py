from django.contrib import admin

# Register your models here.
from .models import *

admin.register(Course, Topic, Field)(admin.ModelAdmin)