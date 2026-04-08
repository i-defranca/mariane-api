from api.filters import PeriodFilter
from api.models import Period
from api.serializers import PeriodCreateSerializer, PeriodListSerializer
from api.services import create_period, update_period
from api.views.mixins import BaseViewSet, UserOwnerMixin


class PeriodViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Period.objects.all()

    filterset_class = PeriodFilter

    serializers = {
        'list': PeriodListSerializer,
        'create': PeriodCreateSerializer,
    }

    actions = {
        'destroy': True,
        'create': create_period,
        'update': update_period,
    }
