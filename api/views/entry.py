from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import EntryFilter
from api.models import Entry
from api.serializers import EntryCreateSerializer, EntryListSerializer
from api.services import create_entry
from api.views.utils import res


class EntryViewSet(CreateModelMixin, GenericViewSet):
    queryset = Entry.objects.all().prefetch_related('metric', 'option', 'period')

    filterset_class = EntryFilter

    def get_serializer_class(self):  # type: ignore[override]
        if self.action == 'create':
            return EntryCreateSerializer
        return EntryListSerializer

    def list(self, request):
        user = request.user

        if 'month' not in request.query_params:
            return res(status=400)

        qs = self.filter_queryset(self.get_queryset().filter(user=user))
        return res(self.get_serializer(qs, many=True).data)

    def create(self, request):
        sr = self.get_serializer(data=request.data)
        sr.is_valid(raise_exception=True)

        return res(
            EntryListSerializer(create_entry(**sr.validated_data)).data,
            status=201,
        )
