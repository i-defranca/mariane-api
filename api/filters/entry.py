from datetime import date, timedelta

import django_filters as df
from rest_framework.exceptions import ParseError

from api.models import Entry


class EntryFilter(df.FilterSet):
    month = df.CharFilter(method='filter_month', required=True)
    metric = df.CharFilter(field_name='metric__slug')
    period = df.BooleanFilter(method='filter_period')

    class Meta:
        model = Entry
        fields = ['month', 'metric', 'period']

    def filter_month(self, queryset, _, value):
        try:
            y, m = map(int, value.split('-'))

            first = date(y, m, 1)

            y = y if m < 12 else y + 1
            m = m + 1 if m < 12 else 1

            last = date(y, m, 1) - timedelta(days=1)

            return queryset.filter(entry_date__range=(first, last))
        except ValueError as e:
            raise ParseError() from e

    def filter_period(self, queryset, _, value):
        return queryset.filter(period__isnull=not value)
