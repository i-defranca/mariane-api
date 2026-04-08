from api.filters import PeriodFilter
from api.models import Period
from api.serializers import PeriodListSerializer
from api.views.mixins import BaseViewSet, UserOwnerMixin


class PeriodViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Period.objects.all()

    serializers = {'list': PeriodListSerializer}
    filterset_class = PeriodFilter
