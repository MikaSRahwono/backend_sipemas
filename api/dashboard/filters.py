import django_filters

from api.marketplace.models import Topic
from .models import *

class ActivityFilter(django_filters.FilterSet):
    topic__title = django_filters.CharFilter(lookup_expr='icontains')
    supervisees__email = django_filters.CharFilter(lookup_expr='icontains')
    supervisors__email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = {
            'course_id': ['exact'],
            'topic__title': ['exact'],
            'created_on': ['exact'],
            'supervisees__email': ['exact'],
            'supervisors__email': ['exact'],
            'is_completed': ['exact'],
        }