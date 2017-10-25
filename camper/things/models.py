import uuid
from django.db import models


class Thing(models.Model):
    TYPES = (
        ('sensor', 'Sensor'),
        ('switch', 'Switch'),
        ('rotor', 'Rotor'),
    )

    id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    type = models.CharField(max_length=32, null=False, blank=False, choices=TYPES)

    # input_channels = models.ManyToManyField('channels.InputChannel', blank=True)
    # output_channels = models.ManyToManyField('channels.OutputChannel', blank=True)
    values = models.ManyToManyField('channels.Value', blank=True)

    def __str__(self):
        return self.name

    __repr__ = __str__

