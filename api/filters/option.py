from django_filters import CharFilter, FilterSet

from api.models import MetricOption as Option


class OptionFilter(FilterSet):
    metric = CharFilter(field_name='metric__slug', required=True)

    class Meta:
        model = Option
        fields = ['metric']
