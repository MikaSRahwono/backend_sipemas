from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'academic'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'fields', FieldViewSet, basename='fields')

urlpatterns = [
    path(r'', include(router.urls)),
]