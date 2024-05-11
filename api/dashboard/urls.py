from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

app_name = 'dashboard'

router = DefaultRouter()
router.register(r'secretary', SecretaryDashboardViewSet, basename='secretary')
router.register(r'lecturer', LecturerDashboardViewSet, basename='lecturer')

urlpatterns = [
    path(r'', include(router.urls)),
]