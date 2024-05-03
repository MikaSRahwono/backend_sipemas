from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'academic'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'fields', FieldViewSet, basename='fields')
router.register(r'activity_steps', ActivityStepViewSet, basename='acticity_steps')
router.register(r'step_assignment_components', StepComponentViewSet, basename='step_assignment_components')

urlpatterns = [
    path(r'', include(router.urls)),
]
