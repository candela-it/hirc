import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings

from core.model_utilities import TimeStampedModelMixin


class CustomUser(User):
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)


class RequestStatus(TimeStampedModelMixin, models.Model):
    title = models.CharField(max_length=15)


class RequestDate(TimeStampedModelMixin, models.Model):
    date = models.DateField(help_text='Date of the request')
    time = models.TimeField(
        null=True, blank=True, help_text='Time of the request'
    )
    imagery_request = models.ForeignKey('ImageryRequest')


class ImageryRequest(TimeStampedModelMixin, models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created'
    )
    area_of_interest = models.PolygonField(
        srid=4326, help_text='Imagery request area of interest'
    )
    status = models.ForeignKey(
        'RequestStatus', default=1, help_text='Status of the imagery request'
    )
    title = models.CharField(
        max_length=50, help_text='Title of the imagery request'
    )
    description = models.TextField(
        blank=True, help_text='Description of the imagery request'
    )
    project_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='project_lead'
    )

    question_set = models.ForeignKey('questions.QuestionSet', null=True)

    # default manager
    objects = models.GeoManager()
