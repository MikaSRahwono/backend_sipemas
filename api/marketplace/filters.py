import django_filters
from .models import *

class TopicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    supervisors__email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = {
            'title': ['exact'],
            'num_of_people': ['exact'],
            'is_open': ['exact'],
            'fields__code': ['exact'],
            'supervisors__email': ['exact']
        }

class ApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = Application
        fields = {
            'is_approved': ['exact'],
        }