from django.db import models
from django.conf import settings


class Channel(models.Model):
    class Meta:
        abstract = True

    id = models.SlugField(null=False, blank=False, primary_key=True)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Channel {}'.format(
            self.id
        )

    __repr__ = __str__


class InputChannel(Channel):
    def notify(self, data):
        values = []

        for thing in self.things.all():
            thing.notify(data)

        return values


class OutputChannel(Channel):
    destination_url = models.URLField(null=False, blank=False)

