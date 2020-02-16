import django_filters
from django.db.models import Q
from .models import Case


class CaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Naam', method='filter_by_multiple_fields')

    class Meta:
        model = Case
        fields = ['name', 'case_type', 'current_phase', 'assignee']

    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)

        self.filters['case_type'].label = 'Zaaktype'
        self.filters['current_phase'].label = 'Huidige fase'
        self.filters['assignee'].label = 'Behandelaar'

    def filter_by_multiple_fields(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) | Q(name__icontains=value)
        )
