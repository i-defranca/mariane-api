from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Metric
from api.serializers import MetricListSerializer, MetricRetrieveSerializer


class MetricViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    queryset = Metric.objects.all().prefetch_related('options').order_by('slug')

    lookup_field = 'slug'

    def get_serializer_class(self):  # type: ignore[override]
        if self.action == 'retrieve':
            return MetricRetrieveSerializer
        return MetricListSerializer
