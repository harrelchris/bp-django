from datetime import timedelta
from functools import cached_property

from common.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser, BaseModel):
    is_verified = models.BooleanField(default=False)


class EmailVerificationToken(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @cached_property
    def to_string(self):
        return self.uuid

    @property
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(hours=24)
