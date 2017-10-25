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
        for value in self.values.all():
            value.update(data)
            values.append(value)
        return values


class Value(models.Model):
    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    description = models.TextField(null=True, blank=True)
    channel = models.ForeignKey('InputChannel', null=False, blank=False, related_name='values')
    json_path = models.CharField(max_length=128, null=False, blank=False, default='$.value')
    data = models.TextField(null=True, blank=True)
    date_last_updated = models.DateTimeField(null=False, blank=False, default=now)

    def update(self, original_data):
        data = None
        for part in self.json_path.split('.'):
            if part == '$':
                data = original_data
            else:
                data = data[part]
        self.data = data
        self.date_last_updated = now()
        self.save()
        Event.objects.create(
            value=self,
            data=self.data
        )

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


# class OutputChannel(Channel):
#     destination_url = models.URLField(null=False, blank=False)


# class Transformer(models.Model):
#     TEMPLATE_HEADER = '{% load core %}\n'

#     id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
#     script = models.TextField(null=False, blank=False, default='{{ data|json }}')

#     def feed(self, data):
#         template = Template(Transformer.TEMPLATE_HEADER + self.script)
#         transformed = template.render(Context(dict(data=data)))
#         return json.loads(transformed)

