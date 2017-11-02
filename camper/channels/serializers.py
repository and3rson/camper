from rest_framework import serializers
from . import models


class InputChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputChannel
        fields = ('id', 'url', 'description',)


class NotifySerializer(serializers.Serializer):
    class Meta:
        fields = ('data',)

    data = serializers.JSONField(required=True)


# value_url = serializers.HyperlinkedRelatedField(view_name='value-detail', source='value', read_only=True)
# value_id = serializers.PrimaryKeyRelatedField(source='value', read_only=True)
# value = ValueSerializer(many=False)


# class OutputChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.OutputChannel
#         fields = ('id', 'url', 'type', 'description', 'transformer', 'destination_url')

