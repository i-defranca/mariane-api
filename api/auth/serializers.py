from rest_framework import serializers

from api.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'cycle_day', 'cycle_phase']
