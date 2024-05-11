from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

app_name = 'dashboard'

router = DefaultRouter()
router.register(r'secretary', SecretaryDashboardViewSet, basename='secretary')

urlpatterns = [
    path(r'', include(router.urls)),
]