import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

import reversion

from core.model_utilities import TimeStampedModelMixin


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)


class RequestStatus(TimeStampedModelMixin, models.Model):
    title = models.CharField(max_length=15)

    def __unicode__(self):
        return self.title


class RequestDate(TimeStampedModelMixin, models.Model):
    date = models.DateField(help_text='Date of the request')
    time = models.TimeField(
        null=True, blank=True, help_text='Time of the request'
    )
    imagery_request = models.ForeignKey('ImageryRequest')

    def __unicode__(self):
        if self.time:
            return u'{} ({})'.format(self.date, self.time)
        else:
            return u'{}'.format(self.date)

# register model with reversion
reversion.register(RequestDate)


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
    request_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='request_lead'
    )

    question_set = models.ForeignKey('questions.QuestionSet', null=True)

    # default manager
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_request', args=[str(self.id)])

    def questions_and_answers(self):
        questions = self.question_set.questions.all().values(
            'id', 'text'
        )
        answers = self.answer_set.all().values(
            'id', 'question', 'text'
        )
        for i, qu in enumerate(questions):
            for an in answers:
                if an['question'] == qu['id']:
                    questions[i].update({'answer': an})
                    break
            else:
                questions[i].update({'answer': {'text': 'No answer'}})
        return questions


# register model with reversion
reversion.register(ImageryRequest)
