import uuid

from django.db import models

from . import managers


class BaseModel(models.Model):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = managers.BaseManager()

    class Meta:
        abstract = True
