from rest_framework.routers import DefaultRouter

from api.views import EntryViewSet, MetricViewSet, PeriodViewSet

router = DefaultRouter()
router.register('entries', EntryViewSet, basename='entry')
router.register('metrics', MetricViewSet, basename='metric')
router.register('periods', PeriodViewSet, basename='period')
