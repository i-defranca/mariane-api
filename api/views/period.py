from rest_framework.viewsets import GenericViewSet

from api.filters import PeriodFilter
from api.models import Period
from api.serializers import PeriodListSerializer
from api.views.mixins import ListMixin, UserOwnerMixin


class PeriodViewSet(UserOwnerMixin, ListMixin, GenericViewSet):
    queryset = Period.objects.all()

    serializers = {'list': PeriodListSerializer}
    filterset_class = PeriodFilter
