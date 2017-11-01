from rest_framework import serializers
from . import models
from camper.channels.serializers import ValueSerializer  # , OutputChannelSerializer
from camper.channels.models import Value


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thing
        fields = ('id', 'url', 'name', 'type', 'is_alive', 'values_ids', 'values')  # , 'output_channels')
        read_only_fields = ('values', 'is_alive')

    # input_channels = InputChannelSerializer(many=True)
    # output_channels = OutputChannelSerializer(many=True)
    values_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Value.objects.all(), source='values')
    # values = serializers.(many=True, queryset=Value.objects.all())
    values = ValueSerializer(many=True, read_only=True)

