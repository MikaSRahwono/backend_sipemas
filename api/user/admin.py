from django.contrib import admin

# Register your models here.
from .models import *

admin.register(
    Organization,
    UserDetail,
    UserProfile,
    Experience,)(admin.ModelAdmin)