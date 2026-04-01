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
        opts = obj.options
        user = self.context['request'].user

        global_f = Q(user__isnull=True)
        user_f = Q(user=user) | global_f

        opts = opts.filter(user_f if user.is_authenticated else global_f)

        return [{'id': v.id, 'label': v.label} for v in opts]

    class Meta:
        model = Metric
        fields = ['slug', 'custom', 'multiple', 'options']
