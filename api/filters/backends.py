from django_filters.rest_framework import DjangoFilterBackend


class ActionAwareBackend(DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        allowed = getattr(view, 'filterset_actions', None)

        if allowed and getattr(view, 'action', None) not in allowed:
            return None

        return super().get_filterset_class(view, queryset)
