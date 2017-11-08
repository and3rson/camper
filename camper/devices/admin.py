from django.contrib import admin
from . import models


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name')


admin.site.register(models.Device, DeviceAdmin)

