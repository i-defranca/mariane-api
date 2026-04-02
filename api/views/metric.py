from django.db.models import Prefetch, Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Metric, MetricOption
from api.serializers import MetricListSerializer, MetricRetrieveSerializer


class MetricViewSet(ReadOnlyModelViewSet):
    lookup_field = 'slug'

    def get_serializer_class(self):  # type: ignore[override]
        if self.action == 'retrieve':
            return MetricRetrieveSerializer

        return MetricListSerializer

    def get_queryset(self):
        qry = Metric.objects.all()

        if self.action == 'retrieve':
            qry = qry.prefetch_related(
                Prefetch(
                    'options',
                    queryset=MetricOption.objects.filter(
                        Q(user=self.request.user) | Q(user__isnull=True)
                    ),
                )
            )

        return qry.order_by('slug')
