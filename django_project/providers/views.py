import logging
LOGGER = logging.getLogger(__name__)

from rest_framework import viewsets
# from rest_framework.response import Response


from .models import ProviderResponse
from .serializers import ProviderResponseSerializer


class ProviderResponseViewSet(viewsets.ModelViewSet):

    model = ProviderResponse
    filter_fields = ['imagery_request']
    serializer_class = ProviderResponseSerializer
