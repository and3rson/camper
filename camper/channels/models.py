import uuid
import json
from django.db import models
from django.template import Context, Template
from django.core.validators import MinValueValidator
from django.utils.timezone import now


class Channel(models.Model):
    class Meta:
        abstract = True

    id = models.SlugField(null=False, blank=False, primary_key=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Channel {}'.format(
            self.id
        )

    __repr__ = __str__


class InputChannel(Channel):
    def notify(self, data):
        values = []
        changed = []

        for value in self.values.all():
            values.append(value)
            changed.append(value.update(data))

        for value, has_changed in zip(values, changed):
            value.save()
            if has_changed:
                Event.objects.create(
                    value=value,
                    data=value.data
                )

        return values


class ValueUpdateException(Exception):
    def __init__(self, value, e):
        self.value = value
        self.reason = '{}: {}'.format(e.__class__.__name__, str(e))
        super().__init__(str(e))


class Value(models.Model):
    class Meta:
        unique_together = ('id', 'channel')

    VALUE_TYPES = (
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('speed', 'Speed'),
        ('power', 'Power'),
        ('distance', 'Distance'),
        ('other', 'Other'),
        ('brightness', 'Brightness'),
    )

    id = models.SlugField(null=False, blank=False, primary_key=True, editable=True)
    description = models.TextField(null=True, blank=True)
    channel = models.ForeignKey('InputChannel', null=False, blank=False, related_name='values')
    json_path = models.CharField(max_length=128, null=False, blank=False, default='$.value')
    data = models.TextField(null=True, blank=True)
    date_last_updated = models.DateTimeField(null=False, blank=False, default=now)
    value_type = models.CharField(max_length=32, null=False, blank=False, choices=VALUE_TYPES)

    def update(self, original_data):
        try:
            data = None
            for part in self.json_path.split('.'):
                if part == '$':
                    data = original_data
                else:
                    data = data[part]
        except Exception as e:
            raise ValueUpdateException(self, e)
        has_changed = self.data != data
        self.data = data
        self.date_last_updated = now()
        return has_changed

    def __str__(self):
        return 'Channel {}, value {}'.format(
            self.channel.id,
            self.id
        )

    __repr__ = __str__


class Event(models.Model):
    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    date_created = models.DateTimeField(null=False, blank=False, default=now)
    value = models.ForeignKey('Value', null=False, blank=False)
    data = models.TextField(null=True, blank=True)


class OutputChannel(Channel):
    destination_url = models.URLField(null=False, blank=False)


# class Transformer(models.Model):
#     TEMPLATE_HEADER = '{% load core %}\n'

#     id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
#     script = models.TextField(null=False, blank=False, default='{{ data|json }}')

#     def feed(self, data):
#         template = Template(Transformer.TEMPLATE_HEADER + self.script)
#         transformed = template.render(Context(dict(data=data)))
#         return json.loads(transformed)

