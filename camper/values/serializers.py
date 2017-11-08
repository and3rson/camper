from . import models
from rest_framework import serializers
from camper.controls.serializers import ControlSerializer


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = (
            'id', 'url', 'value_type', 'name', 'device', 'json_path',
            'ttl_seconds', 'data', 'date_last_updated', 'is_alive', 'last_error', 'controls', 'controls'
        )
        read_only_fields = ('date_last_updated', 'last_error', 'last_alive_state', 'is_alive')

    controls = ControlSerializer(many=True)


class ValueSetSerializer(serializers.Serializer):
    class Meta:
        fields = ('data',)

    data = serializers.JSONField(required=True)


class ValueLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ValueLog
        fields = (
            'id', 'value', 'data', 'date_created'
        )

