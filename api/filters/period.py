from django.db.models import Q
from django_filters import CharFilter, FilterSet

from api.filters.utils import parse
from api.models import Period


class PeriodFilter(FilterSet):
    month = CharFilter(method='filter_month', required=True)

    class Meta:
        model = Period
        fields = ['month']

    def filter_month(self, queryset, _, value):
        first, last = parse.month(value)

        def qry(ended=True):
            return {'end_date__isnull': not ended, 'start_date__lte': last}

        complete = {**qry(), 'end_date__gte': first}

        return queryset.filter(Q(**complete) | Q(**qry(False)))
