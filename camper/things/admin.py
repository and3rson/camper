from django.contrib import admin
from . import models


class ThingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type')


admin.site.register(models.Thing, ThingAdmin)

