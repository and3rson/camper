import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Event(models.Model):
    TYPES = (
        ('thing:change', 'Thing changed'),
        ('value:change', 'Value changed'),
    )

    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    type = models.CharField(max_length=32, null=False, blank=False, choices=TYPES)
    date_created = models.DateTimeField(null=False, blank=False, default=now)
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.SlugField()
    object = GenericForeignKey('object_type', 'object_id')
    # object = models.ForeignKey('Value', null=False, blank=False)
    data = JSONField(null=True, blank=True)

