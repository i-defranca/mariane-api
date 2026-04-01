from rest_framework import serializers

from api.models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'slug', 'custom', 'multiple']
