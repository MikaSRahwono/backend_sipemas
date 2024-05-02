from django.contrib import admin

# Register your models here.
from .models import *

admin.register(
    Activity,
    )(admin.ModelAdmin)