import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Event(models.Model):
    TYPES = (
        ('device:change', 'Device changed'),
        ('value:change', 'Value changed'),
    )

    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    type = models.CharField(max_length=32, null=False, blank=False, choices=TYPES)
    date_created = models.DateTimeField(null=False, blank=False, default=now)
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.SlugField()
    object = GenericForeignKey('object_type', 'object_id')
    data = JSONField(null=True, blank=True)

