from json import loads
from rest_framework import serializers
from . import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'url', 'type', 'date_created', 'object_type', 'object_id', 'data')

    object_type = serializers.SerializerMethodField()
    # data = serializers.SerializerMethodField()

    def get_object_type(self, obj):
        return obj.object_type.model

    # def get_data(self, obj):
    #     if isinstance(obj.data, str):
    #         return loads(obj.data)
    #     return obj.data

