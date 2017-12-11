from django.db import models
from model_utils.managers import InheritanceManager


class Control(models.Model):
    id = models.SlugField(null=False, blank=False, primary_key=True, editable=True, max_length=100)
    name = models.CharField(max_length=128, null=False, blank=False)
    owner = models.ForeignKey('auth.User', null=False, blank=False, related_name='controls')
    value = models.ForeignKey('values.Value', null=False, blank=False, related_name='controls')

    objects = InheritanceManager()

    @property
    def type(self):
        raise NotImplementedError()


class SwitchControl(Control):
    is_enabled = models.BooleanField(null=False, default=False)

    @property
    def type(self):
        return 'switch'


class RangeControl(Control):
    min_value = models.FloatField(null=False, blank=False)
    max_value = models.FloatField(null=False, blank=False)
    step = models.FloatField(null=False, blank=False)
    is_float = models.BooleanField(null=False, default=True)

    @property
    def type(self):
        return 'range'

