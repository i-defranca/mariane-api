from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Metric
from api.serializers import MetricSerializer


class MetricViewSet(ReadOnlyModelViewSet):
    queryset = Metric.objects.all().order_by('slug')
    serializer_class = MetricSerializer

    lookup_field = 'slug'
