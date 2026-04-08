from django.db.models import Prefetch, Q

from api.models import Metric, MetricOption
from api.serializers import MetricListSerializer, MetricRetrieveSerializer
from api.views.mixins import BaseViewSet


class MetricViewSet(BaseViewSet):
    lookup_field = 'slug'

    serializers = {
        'list': MetricListSerializer,
        'retrieve': MetricRetrieveSerializer,
    }

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
