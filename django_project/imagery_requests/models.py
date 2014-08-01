import logging
logger = logging.getLogger(__name__)

import datetime

from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, BaseUserManager
)
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils import timezone

import reversion

from core.model_utilities import TimeStampedModelMixin


class CustomUserManager(BaseUserManager):
    def _create_user(
            self, username, email, password, is_staff, is_superuser,
            **extra_fields):

        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(
            username, email, password, True, True, **extra_fields
        )


class CustomUser(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(
        max_length=30, unique=True,
        help_text=(
            'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ '
            'only.'
        ),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid'
            )
        ]
    )
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    email = models.EmailField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return unicode(self.username)

    def get_full_name(self):
        return u'{} ({})'.format(self.username, self.email)

    def get_short_name(self):
        return unicode(self.username)

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True


class RequestStatus(TimeStampedModelMixin, models.Model):
    title = models.CharField(max_length=15)

    def __unicode__(self):
        return self.title


class RequestDate(TimeStampedModelMixin, models.Model):
    date = models.DateField(help_text='Date of the request')
    time = models.TimeField(
        null=True, blank=True, help_text='Time of the request',
        default=datetime.time(0, 00, 00)
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
    area_of_interest = models.MultiPolygonField(
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

    def as_geojson(self):
        return {
            'id': self.pk,
            'polygon': self.area_of_interest.geojson,
            'title': self.title,
            'status': self.status.title
        }

# register model with reversion
reversion.register(ImageryRequest)
