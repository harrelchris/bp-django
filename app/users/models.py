from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from common.models import BaseModel


class User(AbstractUser, BaseModel):
    is_verified = models.BooleanField(default=False)


class EmailVerificationToken(BaseModel):
    # UUID already exists in the common.models.BaseModel and is used as the token
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(days=1)
