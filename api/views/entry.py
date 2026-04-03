from rest_framework.viewsets import GenericViewSet

from api.filters import EntryFilter
from api.models import Entry
from api.serializers import EntryListSerializer
from api.views.utils import res


class EntryViewSet(GenericViewSet):
    queryset = Entry.objects.all().prefetch_related('metric', 'option', 'period')
    serializer_class = EntryListSerializer

    filterset_class = EntryFilter

    def list(self, request):
        user = request.user

        if 'month' not in request.query_params:
            return res(status=400)

        qs = self.filter_queryset(self.get_queryset().filter(user=user))
        return res(self.serializer_class(qs, many=True).data)
