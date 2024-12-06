from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Manager, InstrumentPlatform


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ManagerSerializer(serializers.ModelSerializer):
    instrument = serializers.CharField(required=False, source="instrument_platform_id")
    platform = serializers.CharField(required=False)

    # instrument_platform_id = serializers.IntegerField(required=False, default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        attrs = super().validate(attrs)
        instrument_name = attrs.pop('instrument', None)
        platform__name = attrs.pop('platform', None)
        instrument_platform = InstrumentPlatform.objects.filter(instrument__name=instrument_name,
                                                                platform__name=platform__name).first()
        if instrument_platform:
            attrs['instrument_platform_id'] = instrument_platform.pk
        else:
            raise ValidationError('Нет такой связки')
        return attrs

        # if not attrs.get('instrument_platform_id'):
        #     instrument_platform = InstrumentPlatform.objects.filter(instrument__name=instrument_name,
        #                                                             platform__name=platform__name).first()
        #     if instrument_platform:
        #         attrs['instrument_platform_id'] = instrument_platform.pk
        #     else:
        #         raise ValidationError('Нет такой связки')
        # return attrs


    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Manager
        # fields = '__all__'
        fields = [
            "instrument",
            "platform",
            "id",
            # "instrument_platform_id",
            "order_spread",
            "order_step",
            "start_step",
            "order_size",
            "grid_depth",
            "grid_side",
            "user"
        ]

'''
{
    "instrument": "BTC-PERPETUAL",
    "platform": "deribit",
    "instrument_platform_id": 1,
    "order_spread": 1,
    "order_step": 1,
    "start_step": 1,
    "order_size": 1,
    "grid_depth": 1,
    "grid_side": 1
}
'''