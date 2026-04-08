from api.filters import OptionFilter
from api.models import MetricOption as Option
from api.serializers import OptionCreateSerializer, OptionListSerializer
from api.services import create_option
from api.views.mixins import BaseViewSet, UserOwnerMixin


class OptionViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Option.objects.all().prefetch_related('metric')

    filterset_class = OptionFilter

    serializers = {
        'list': OptionListSerializer,
        'create': OptionCreateSerializer,
    }

    actions = {
        'destroy': True,
        'create': create_option,
    }
