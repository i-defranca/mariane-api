from rest_framework import serializers

from api.models import Metric


class MetricListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple']


class MetricRetrieveSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple', 'options']
