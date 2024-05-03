from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'marketplace'

router = DefaultRouter()
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'applications', ApplicationsViewSet, basename='applications')
router.register(r'application_approvals', ApplicationApprovalViewSet, basename='application_approvals')
router.register(r'topic_request_approvals', TopicRequestApprovalViewSet, basename='topic_approvals')


urlpatterns = [
    path(r'', include(router.urls)),
]