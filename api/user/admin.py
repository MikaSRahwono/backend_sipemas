from django.contrib import admin


from .models import *

admin.register(
    Organization,
    UserDetail,
    UserProfile,
    Experience,)(admin.ModelAdmin)