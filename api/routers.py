from rest_framework.routers import DefaultRouter

from api.views import MetricViewSet

router = DefaultRouter()
router.register('metrics', MetricViewSet, basename='metric')
