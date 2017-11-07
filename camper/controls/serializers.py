from rest_framework import serializers
from . import models


class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Control
        fields = (
            'id', 'url', 'name', 'owner', 'type'
        )
        read_only_fields = ('owner',)

    def to_representation(self, instance):
        SERIALIZERS = {
            models.SwitchControl: SwitchControlSerializer,
            models.RangeControl: RangeControlSerializer
        }
        serializer_class = SERIALIZERS[instance.__class__]
        return serializer_class(instance=instance, context=self.context).data

class SwitchControlSerializer(serializers.ModelSerializer):
    class Meta(ControlSerializer.Meta):
        model = models.SwitchControl
        fields = ControlSerializer.Meta.fields + ('is_enabled',)


class RangeControlSerializer(serializers.ModelSerializer):
    class Meta(ControlSerializer.Meta):
        model = models.RangeControl
        fields = ControlSerializer.Meta.fields + ('min_value', 'max_value', 'default_value', 'step', 'is_float')

