import logging
logger = logging.getLogger(__name__)

from django.db import models

import reversion

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

# register model with reversion
reversion.register(Question)


class Answer(TimeStampedModelMixin, models.Model):
    text = models.TextField(help_text='Answer text')
    question = models.ForeignKey('Question')
    imagery_request = models.ForeignKey('imagery_requests.ImageryRequest')

    def __unicode__(self):
        return self.text

# register model with reversion
reversion.register(Answer)
