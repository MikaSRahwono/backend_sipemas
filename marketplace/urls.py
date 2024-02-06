from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'marketplace'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

topic_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
topic_router.register(r'topics', TopicViewSet, basename='topics')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(topic_router.urls)),
]