from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .models import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        member = Member.objects.create(
            **validated_data
        )
        return member

    def update(self, instance, validated_data):
        instance._member, created = Member.objects.get_or_create(email__exact=validated_data['email']
                                                                 )
        instance.email = validated_data.get('email', None)
        instance.phone = validated_data.get('phone', None) if validated_data.get(
            'phone', None) else instance.phone
        instance.name = validated_data.get('name', None)
        instance.birthday = validated_data.get('birthday', None)
        instance.gender = validated_data.get('gender', None)
        instance.address = validated_data.get('address', None)
        instance.oauthid = validated_data.get('oauthid', None)
        instance.password = validated_data.get('password', None)
        instance.save()
        return instance
