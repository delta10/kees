import django_filters
from django.forms import RadioSelect
from django.db.models import Q
from .models import Case, PredefinedFilter

STATUS_CHOICES = (
    ('open', 'Open'),
    ('closed', 'Gesloten'),
    ('all', 'Alle'),
)


class CaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Naam', method='filter_by_multiple_fields')
    predefined = django_filters.ModelChoiceFilter(label='', queryset=PredefinedFilter.objects, widget=RadioSelect,
                                                  method='filter_by_predefined', empty_label='Alle zaken')
    status = django_filters.ChoiceFilter(label='Status', choices=STATUS_CHOICES,
                                         method='filter_status', empty_label=None, null_value='open')

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

    def filter_by_predefined(self, queryset, name, value):
        if value == 'all':
            return queryset

        if value == 'mine':
            return queryset.filter(assignee=self.request.user)

        if value.args:
            return queryset.filter(data__contains=value.args)

        return queryset

    def filter_status(self, queryset, name, value):
        if value == 'open':
            return queryset.filter(current_phase__isnull=False)

        if value == 'closed':
            return queryset.filter(current_phase__isnull=True)

        return queryset
