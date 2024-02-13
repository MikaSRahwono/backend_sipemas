from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = 'user'

router = DefaultRouter()
router.register(r'', UsersViewSet, basename='student')

urlpatterns = [
    path(r'', include(router.urls)),
]