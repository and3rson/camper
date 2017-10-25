from django.contrib import admin
from . import models


class InputChannelAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


# class OutputChannelAdmin(admin.ModelAdmin):
#     list_display = ('__str__',)


admin.site.register(models.InputChannel, InputChannelAdmin)
# admin.site.register(models.OutputChannel, OutputChannelAdmin)

