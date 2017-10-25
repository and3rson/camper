from rest_framework import serializers
from . import models


class InputChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputChannel
        fields = ('id', 'url', 'description',)


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = ('id', 'url', 'description', 'channel', 'json_path', 'data', 'date_last_updated')
        read_only_fields = ('id', 'date_last_updated')


class NotifySerializer(serializers.Serializer):
    class Meta:
        fields = ('data',)

    data = serializers.JSONField(required=True)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'url', 'value_id', 'data')

    # value_url = serializers.HyperlinkedRelatedField(view_name='value-detail', source='value', read_only=True)
    value_id = serializers.PrimaryKeyRelatedField(source='value', read_only=True)
    # value = ValueSerializer(many=False)


# class OutputChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.OutputChannel
#         fields = ('id', 'url', 'type', 'description', 'transformer', 'destination_url')

