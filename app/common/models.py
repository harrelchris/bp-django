import uuid

from django.db import models

from common.managers import BaseManager


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    class Meta:
        abstract = True
