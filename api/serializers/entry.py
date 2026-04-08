from rest_framework import serializers

from api.models import Entry, Metric, MetricOption, Period


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date']


class EntryListSerializer(serializers.ModelSerializer):
    metric = serializers.SlugRelatedField(many=False, read_only=True, slug_field='slug')
    option = serializers.StringRelatedField(many=False)
    period = PeriodSerializer(many=False, read_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'metric', 'option', 'period', 'entry_date', 'created_at']


class EntryCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    metric = serializers.SlugRelatedField(
        slug_field='slug', queryset=Metric.objects.all()
    )
    option = serializers.SlugRelatedField(
        slug_field='label', queryset=MetricOption.objects.all()
    )
    entry_date = serializers.DateField(required=False)
