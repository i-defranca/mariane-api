from api.filters import EntryFilter
from api.models import Entry
from api.serializers import EntryCreateSerializer, EntryListSerializer
from api.services import create_entry
from api.views.mixins import BaseViewSet, UserOwnerMixin


class EntryViewSet(UserOwnerMixin, BaseViewSet):
    queryset = Entry.objects.all().prefetch_related('metric', 'option', 'period')

    filterset_class = EntryFilter

    serializers = {
        'list': EntryListSerializer,
        'create': EntryCreateSerializer,
    }

    actions = {
        'destroy': True,
        'create': create_entry,
    }
