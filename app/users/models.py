from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class User(AbstractUser, BaseModel):
    is_verified = models.BooleanField(default=False)
