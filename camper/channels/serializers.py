from json import loads
from rest_framework import serializers
from . import models


class InputChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputChannel
        fields = ('id', 'url', 'description',)


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = ('id', 'url', 'value_type', 'description', 'channel', 'ttl_seconds', 'json_path', 'data', 'date_last_updated')
        read_only_fields = ('date_last_updated',)

    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        # TODO: Fix JSON field!
        try:
            return loads(obj.data)
        except:
            return obj.data

    # data = serializers.JSONField()


class NotifySerializer(serializers.Serializer):
    class Meta:
        fields = ('data',)

    data = serializers.JSONField(required=True)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'url', 'type', 'date_created', 'object_type', 'object_id', 'data')

    object_type = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_object_type(self, obj):
        return obj.object_type.model

    def get_data(self, obj):
        if isinstance(obj.data, str):
            return loads(obj.data)
        return obj.data

    # value_url = serializers.HyperlinkedRelatedField(view_name='value-detail', source='value', read_only=True)
    # value_id = serializers.PrimaryKeyRelatedField(source='value', read_only=True)
    # value = ValueSerializer(many=False)


# class OutputChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.OutputChannel
#         fields = ('id', 'url', 'type', 'description', 'transformer', 'destination_url')

