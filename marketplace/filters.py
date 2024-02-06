import django_filters
from .models import Topic

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