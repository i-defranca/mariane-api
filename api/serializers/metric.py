from rest_framework import serializers

from api.models import Metric, MetricOption


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricOption
        fields = ['id', 'label']


class MetricListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple']


class MetricRetrieveSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple', 'options']
