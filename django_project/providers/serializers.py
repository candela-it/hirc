from rest_framework import serializers

from .models import ProviderResponse


class ProviderResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderResponse
        fields = ('id', 'imagery_request', 'provider', 'status')
