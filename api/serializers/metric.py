from django.db.models import Q
from rest_framework import serializers

from api.models import Metric


class MetricListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple']


class MetricRetrieveSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    def get_options(self, obj):
        user = self.context['request'].user
        opts = obj.options.filter(Q(user=user) | Q(user__isnull=True))

        return [{'id': v.id, 'label': v.label} for v in opts]

    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple', 'options']
