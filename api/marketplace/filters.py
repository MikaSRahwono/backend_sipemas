import django_filters
from .models import *

class TopicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    supervisors__email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = {
            'course_id': ['exact'],
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

class ApplicationApprovalFilter(django_filters.FilterSet):
    application__topic__id = django_filters.NumberFilter(ookup_expr='exact')

    class Meta:
        model = ApplicationApproval
        fields = {
            'is_approved': ['exact'],
            'application__topic__id': ['exact'],
        }