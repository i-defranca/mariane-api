from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import EntryFilter
from api.models import Entry
from api.serializers import EntryCreateSerializer, EntryListSerializer
from api.services import create_entry
from api.views.mixins import ListMixin, UserOwnerMixin
from api.views.utils import res


class EntryViewSet(
    CreateModelMixin, DestroyModelMixin, UserOwnerMixin, ListMixin, GenericViewSet
):
    queryset = Entry.objects.all().prefetch_related('metric', 'option', 'period')

    filterset_class = EntryFilter

    serializers = {
        'list': EntryListSerializer,
        'create': EntryCreateSerializer,
    }

    def create(self, request):
        sr = self.get_serializer(data=request.data)
        sr.is_valid(raise_exception=True)

        return res(
            EntryListSerializer(create_entry(**sr.validated_data)).data,
            status=201,
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()

        return res(status=204)
