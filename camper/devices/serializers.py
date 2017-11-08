from rest_framework import serializers
from . import models
from camper.values.serializers import ValueSerializer
from camper.controls.serializers import ControlSerializer


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ('id', 'url', 'name', 'values', 'controls')
        read_only_fields = ('values',)

    values = ValueSerializer(many=True, read_only=True)
    controls = ControlSerializer(many=True, read_only=True)


class NotifySerializer(serializers.Serializer):
    class Meta:
        fields = ('data',)

    data = serializers.JSONField(required=True)

