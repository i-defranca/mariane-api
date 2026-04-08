from django_filters import CharFilter, FilterSet, NumberFilter

from api.filters.utils import parse
from api.models import Entry


class EntryFilter(FilterSet):
    month = CharFilter(method='filter_month', required=True)
    metric = CharFilter(field_name='metric__slug')
    period = NumberFilter(field_name='period')

    class Meta:
        model = Entry
        fields = ['month', 'metric', 'period']

    def filter_month(self, queryset, _, value):
        return queryset.filter(entry_date__range=parse.month(value))
