import django_filters
from .models import Case


class CaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Case
        fields = ['name']