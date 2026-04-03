from rest_framework import serializers

from api.models import Entry, Period


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
        fields = ['metric', 'option', 'period', 'entry_date', 'created_at']
