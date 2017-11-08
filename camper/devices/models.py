from django.db import models


class Device(models.Model):
    id = models.SlugField(null=False, blank=False, primary_key=True)
    owner = models.ForeignKey('auth.User', null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    date_last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def notify(self, data):
        for value in self.values.all():
            value.notify(data)

    __repr__ = __str__

