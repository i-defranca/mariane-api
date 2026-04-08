from rest_framework import serializers

from api.models import Period


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'end_date', 'start_date', 'created_at']


class PeriodCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    end_date = serializers.DateField(required=False)
    start_date = serializers.DateField(required=False)

    def to_representation(self, instance):  # type: ignore
        return PeriodListSerializer(instance).data
