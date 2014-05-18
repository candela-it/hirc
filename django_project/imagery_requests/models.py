import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
