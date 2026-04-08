from api.models import MetricOption as Option
from api.serializers import OptionCreateSerializer
from api.services import create_option
from api.views.mixins import BaseViewSet, UserOwnerMixin


class OptionViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Option.objects.all().prefetch_related('metric')

    serializers = {
        'create': OptionCreateSerializer,
    }

    actions = {
        'destroy': True,
        'create': create_option,
    }
