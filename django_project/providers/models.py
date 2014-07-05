import logging
logger = logging.getLogger(__name__)

from django.db import models

import reversion


class ProviderStatus(models.Model):
    title = models.CharField(max_length=15, unique=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Provider(models.Model):
    name = models.CharField(
        max_length=30, unique=True, help_text='Name of the imagery provider'
    )
    representative = models.ForeignKey(
        'imagery_requests.CustomUser', null=True, blank=True
    )

    def __unicode__(self):
        return self.name


class ProviderResponse(models.Model):
    imagery_request = models.ForeignKey('imagery_requests.ImageryRequest')
    status = models.ForeignKey('providers.ProviderStatus')
    provider = models.ForeignKey(
        'providers.Provider', related_name='responses'
    )

    class Meta:
        unique_together = ('imagery_request', 'status', 'provider')

# register model with reversion
reversion.register(ProviderStatus)
