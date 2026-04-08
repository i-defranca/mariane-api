from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from api.filters import ActionAwareBackend


class UserOwnerMixin:
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BaseViewSet(ModelViewSet):
    filter_backends = [ActionAwareBackend]
    filterset_actions = {'list'}

    pagination = 10
    default_pagination_class = PageNumberPagination
    default_pagination_class.page_size_query_param = 'size'

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if not self.pagination:
                return None
            self._paginator = self.default_pagination_class()
            self._paginator.page_size = self.pagination
        return self._paginator

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.order_by('-id') if not qs.ordered else qs

    def _attr(self, attr):
        return getattr(self, attr, {})

    def get_action(self):
        return self.action.replace('partial_', '')

    def get_serializer_class(self):
        defu = self.serializers.get('list')

        return self.serializers.get(self.get_action(), defu)

    def check_action(self):
        get = self.request.method == 'GET'

        src = self.serializers if get else self._attr('actions')

        if not src.get(self.get_action()):
            raise MethodNotAllowed(self.request.method)

    def list(self, request, *args, **kwargs):
        self.check_action()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.check_action()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.check_action()
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_action()
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.check_action()
        return super().partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        if callable(create := self._attr('actions').get('create')):
            ins = create(**serializer.validated_data)
            serializer.instance = self.instance = ins

    def perform_update(self, serializer):
        if callable(update := self._attr('actions').get('update')):
            ins = update(serializer.instance, **serializer.validated_data)
            serializer.instance = self.instance = ins
