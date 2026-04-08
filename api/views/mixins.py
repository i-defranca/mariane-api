from api.filters import ActionAwareBackend
from api.views.utils import res


class UserOwnerMixin:
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ListMixin:
    filter_backends = [ActionAwareBackend]
    filterset_actions = {'list'}

    def get_serializer_class(self):
        if self.serializers.get(self.action):
            return self.serializers.get(self.action)
        return self.serializers.get('list')

    def list(self, request):
        qs = self.filter_queryset(self.get_queryset())
        return res(self.get_serializer(qs, many=True).data)
