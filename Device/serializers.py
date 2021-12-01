from rest_framework import serializers
from . import models


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device
        fields = '__all__'

    def create(self, validated_data):
        device = models.Device.objects.create(
            **validated_data
        )
        return device

    def update(self, instance, validated_data):
        instance._device, created = models.Device.objects.get_or_create(serialnumber__exact=validated_data['serialnumber']
                                                                        )
        instance.model = validated_data.get('email', None)
        instance.name = validated_data.get('name', None) if validated_data.get(
            'name', None) else instance.name
        instance.bind = validated_data.get('bind', None)
        instance.save()
        return instance
