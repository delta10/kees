import django_filters
from .models import Case


class CaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Naam')

    class Meta:
        model = Case
        fields = ['name', 'case_type', 'current_phase', 'assignee']

    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)

        self.filters['case_type'].label = 'Zaaktype'
        self.filters['current_phase'].label = 'Huidige fase'
        self.filters['assignee'].label = 'Behandelaar'