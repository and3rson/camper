from django.db import models
from django.contrib.postgres.fields import JSONField
from . import backends


class NotificationConfig(models.Model):
    id = models.SlugField(
        null=False, blank=False,
        max_length=100, editable=True,
        primary_key=True
    )

    owner = models.ForeignKey('auth.User', null=False, blank=False, related_name='configs')
    value = models.ForeignKey('values.Value', null=False, blank=False, related_name='configs')
    backend = models.ForeignKey('NotificationBackend', null=False, blank=False, related_name='configs')

    def notify(self):
        self.backend.notify(self.value)


class NotificationBackend(models.Model):
    id = models.SlugField(
        null=False, blank=False,
        max_length=100, editable=True,
        primary_key=True
    )

    owner = models.ForeignKey('auth.User', null=False, blank=False)
    type = models.CharField(max_length=64, null=False, blank=False, choices=[
        (id_, backend.name)
        for id_, backend
        in backends.BACKENDS.items()
    ])
    name = models.CharField(null=False, blank=False, max_length=128)
    config = JSONField(null=False, blank=False, default=dict)

    def notify(self, value):
        backend_class = backends.BACKENDS.get(self.type)
        backend = backend_class()
        backend.notify(self.config, value)

