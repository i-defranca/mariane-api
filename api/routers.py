from rest_framework.routers import DefaultRouter

from api.views import EntryViewSet, MetricViewSet

router = DefaultRouter()
router.register('metrics', MetricViewSet, basename='metric')
router.register('entries', EntryViewSet, basename='entry')
