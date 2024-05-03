import django_filters
from .models import *

class UserFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='icontains')
    # supervisors__email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = {
        }