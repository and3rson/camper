import uuid
from django.db import models


class Thing(models.Model):
    TYPES = (
        ('sensor', 'Sensor'),
        ('switch', 'Switch'),
        ('rotor', 'Rotor'),
    )

    id = models.SlugField(null=False, blank=False, primary_key=True)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    type = models.CharField(max_length=32, null=False, blank=False, choices=TYPES)

    input_channels = models.ManyToManyField('channels.InputChannel', blank=True, related_name='things')
    # output_channels = models.ManyToManyField('channels.OutputChannel', blank=True)
    date_last_updated = models.DateTimeField(null=True, blank=True)
    # values = models.ManyToManyField('channels.Value', blank=True, related_name='things')
    # is_alive = models.BooleanField(null=False, blank=False, default=False)

    # def get_is_alive(self):
    #     return any([value.is_alive() for value in self.values.all()])

    def __str__(self):
        return self.name

    def notify(self, data):
        for value in self.values.all():
            value.notify(data)


    __repr__ = __str__

