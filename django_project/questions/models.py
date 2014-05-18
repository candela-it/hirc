import logging
logger = logging.getLogger(__name__)

from django.db import models

from core.model_utilities import TimeStampedModelMixin


class QuestionSet(TimeStampedModelMixin, models.Model):
    title = models.CharField(max_length=30)
    questions = models.ManyToManyField('Question')

    def __unicode__(self):
        return self.title


class Question(TimeStampedModelMixin, models.Model):
    text = models.TextField(help_text='Question text')

    def __unicode__(self):
        return self.text


class Answer(TimeStampedModelMixin, models.Model):
    text = models.TextField(help_text='Answer text')
    imagery_request = models.ForeignKey('imagery_requests.ImageryRequest')

    def __unicode__(self):
        return self.text
