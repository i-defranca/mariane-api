from rest_framework import serializers

from api.models import Period


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'end_date', 'start_date', 'created_at']
