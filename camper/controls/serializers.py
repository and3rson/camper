from rest_framework import serializers
from . import models
from camper.values.models import Value


class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Control
        fields = (
            'id', 'url', 'name', 'owner', 'type', 'value_id'
        )
        read_only_fields = ('owner',)

    def to_representation(self, instance):
        SERIALIZERS = {
            models.SwitchControl: SwitchControlSerializer,
            models.RangeControl: RangeControlSerializer
        }
        serializer_class = SERIALIZERS.get(instance.__class__)
        if not serializer_class:
            return super().to_representation(instance)
        return serializer_class(instance=instance, context=self.context).data

    value_id = serializers.PrimaryKeyRelatedField(queryset=Value.objects.all(), read_only=False, source='value')


class SwitchControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SwitchControl
        fields = ControlSerializer.Meta.fields + ('is_enabled',)
        read_only_fields = ('owner',)

    value_id = serializers.PrimaryKeyRelatedField(queryset=Value.objects.all(), read_only=False, source='value')


class RangeControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RangeControl
        fields = ControlSerializer.Meta.fields + ('min_value', 'max_value', 'step', 'is_float')
        read_only_fields = ('owner',)

    value_id = serializers.PrimaryKeyRelatedField(queryset=Value.objects.all(), read_only=False)

