from rest_framework import serializers
from authentication.models import ConfirmationCode, User
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

from lotracker.utils.helpers import integers_only
from lotracker.utils.serializers import ValidatorSerializer


class ChangePhoneSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        if User.objects.filter(phone=integers_only(data['phone'])).exists():
            raise ValidationError({'phone': _("Пользователь с таким номером уже существует.")})
        data['phone'] = integers_only(data['phone'])

        return data


class ConfirmChangePhoneSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=20)

    def validate(self, data):
        confirm = ConfirmationCode.objects.filter(
            phone=integers_only(data['phone']),
            code=data['code'],
            is_used=False
        ).first()

        if not confirm:
            raise ValidationError({'code': _("Неверный код подтверждения")})

        data['phone'] = integers_only(data['phone'])
        data['confirm'] = confirm
        return data
