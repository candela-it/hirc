from rest_framework import serializers

from .models import ProviderResponse, Provider, ProviderStatus


class ProviderResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderResponse
        fields = ('id', 'imagery_request', 'provider', 'status')


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'name')


class ProviderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderStatus
        fields = ('id', 'title')
