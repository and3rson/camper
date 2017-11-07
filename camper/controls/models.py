from django.db import models

# TODO: Use polymorphic models from django-model-utils


class Control(models.Model):
    id = models.SlugField(null=False, blank=False, primary_key=True, editable=True)
    name = models.CharField(max_length=32, null=False, blank=False)
    # type = models.CharField(max_length=32, choices=TYPES, null=False, blank=False)


class SwitchControl(Control):
    is_enabled = models.BooleanField(null=False, default=False)


class RangeControl(Control):
    min_value = models.FloatField(null=False, blank=False)
    max_value = models.FloatField(null=False, blank=False)
    default_value = models.FloatField(null=False, blank=False)
    step = models.FloatField(null=False, blank=False)
    is_float = models.BooleanField(null=False, default=True)

