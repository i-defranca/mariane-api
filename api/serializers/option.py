from rest_framework import serializers

from api.models import Metric
from api.models import MetricOption as Option


class OptionListSerializer(serializers.ModelSerializer):
    metric = serializers.SlugRelatedField(many=False, read_only=True, slug_field='slug')

    class Meta:
        model = Option
        fields = ['id', 'metric', 'label']


class OptionCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    metric = serializers.SlugRelatedField(
        slug_field='slug', queryset=Metric.objects.all()
    )
    label = serializers.CharField()

    def to_representation(self, instance):  # type: ignore
        return OptionListSerializer(instance).data
