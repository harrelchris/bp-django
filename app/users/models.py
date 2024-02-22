from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from users.managers import UserManager


class User(AbstractUser, BaseModel):
    objects = UserManager()
