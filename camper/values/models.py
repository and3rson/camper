import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from datetime import timedelta
from camper.events.mixins import EventEmitter


class Value(EventEmitter, models.Model):
    # class Meta:
    #     unique_together = ('id', 'device')

    VALUE_TYPES = (
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('speed', 'Speed'),
        ('power', 'Power'),
        ('distance', 'Distance'),
        ('rotation', 'Rotation'),
        ('brightness', 'Brightness'),
        ('other', 'Other'),
    )

    id = models.SlugField(null=False, blank=False, primary_key=True, editable=True)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    value_type = models.CharField(max_length=32, null=False, blank=False, choices=VALUE_TYPES)
    device = models.ForeignKey('devices.Device', null=False, blank=False, related_name='values')
    json_path = models.CharField(max_length=128, null=False, blank=False, default='$.value')
    ttl_seconds = models.IntegerField(null=False, blank=False, default=15)
    data = JSONField(null=True, blank=True)
    date_last_updated = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(null=True, blank=True)
    last_alive_state = models.BooleanField(default=False)

    def notify(self, original_data):
        try:
            data = None
            for part in self.json_path.split('.'):
                if part == '$':
                    data = original_data
                else:
                    data = data[part]
        except Exception as e:
            self.last_error = str(e)
            event_data = dict(
                last_error=self.last_error
            )
            # self.emit('value:change', last_error=self.last_error)
            success = False
        else:
            self.data = data
            event_data = dict(
                data=data
            )
            success = True
            # self.emit('value:change', data=data)
        self.date_last_updated = now()
        if not self.last_alive_state:
            self.last_alive_state = True
            event_data['is_alive'] = True
        self.emit('value:change', **event_data)
        self.save()
        if success:
            ValueLog.objects.create(
                owner=self.owner,
                value=self,
                data=self.data
            )

    def set(self, data):
        # print('Setting', self, 'data to', data)
        self.data = data
        self.save()
        self.emit('value:change', data=data)

    @property
    def is_alive(self):
        return (self.date_last_updated is not None) and \
            (now() < self.date_last_updated + timedelta(seconds=self.ttl_seconds))

    def check_alive_state(self):
        if self.is_alive != self.last_alive_state:
            print('Value alive state changed to {}'.format(self.is_alive))
            self.last_alive_state = self.is_alive
            self.save()
            self.emit('value:change', is_alive=self.is_alive)

    def __str__(self):
        return '<Device {}, value {}>'.format(
            self.device.id,
            self.id
        )

    __repr__ = __str__


class ValueLog(models.Model):
    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    value = models.ForeignKey('Value', null=False, blank=False, related_name='logs')
    data = JSONField(null=False, blank=False)
    date_created = models.DateTimeField(null=True, blank=True, default=now)

