from django.db.models import Prefetch, Q

from api.models import Metric, MetricOption
from api.serializers import MetricListSerializer, MetricRetrieveSerializer
from api.views.mixins import BaseViewSet


class MetricViewSet(BaseViewSet):
    queryset = Metric.objects.all()
    lookup_field = 'slug'

    serializers = {
        'list': MetricListSerializer,
        'retrieve': MetricRetrieveSerializer,
    }

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                Prefetch(
                    'options',
                    queryset=MetricOption.objects.filter(
                        Q(user=self.request.user) | Q(user__isnull=True)
                    ),
                )
            )

        return qs
