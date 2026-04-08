from api.filters import PeriodFilter
from api.models import Period
from api.serializers import PeriodCreateSerializer, PeriodListSerializer
from api.services import create_period
from api.views.mixins import BaseViewSet, UserOwnerMixin


class PeriodViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Period.objects.all()

    filterset_class = PeriodFilter

    serializers = {
        'list': PeriodListSerializer,
        'create': PeriodCreateSerializer,
    }

    actions = {
        'create': create_period,
    }
