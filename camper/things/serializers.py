from rest_framework import serializers
from . import models
from camper.channels.models import InputChannel
from camper.values.serializers import ValueSerializer  # , OutputChannelSerializer
from camper.values.models import Value


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thing
        fields = ('id', 'url', 'name', 'type', 'input_channels_ids', 'values')  # , 'output_channels')
        read_only_fields = ('values',)

    # input_channels = InputChannelSerializer(many=True)
    # output_channels = OutputChannelSerializer(many=True)
    input_channels_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=InputChannel.objects.all(), source='input_channels')
    # values_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Value.objects.all(), source='values')
    # values = serializers.(many=True, queryset=Value.objects.all())
    values = ValueSerializer(many=True, read_only=True)

