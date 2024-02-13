from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'marketplace'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'fields', FieldViewSet, basename='fields')

topic_router = routers.NestedSimpleRouter(router, r'topics', lookup='topics')
# topic_router.register(r'information', TopicInformationView, basename='topic-information')
topic_router.register(r'applications', ApplicationViewSet, basename='applications')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(topic_router.urls)),
    # path(r'', include(courses_router.urls)),
]