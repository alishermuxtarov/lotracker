from datetime import timedelta

from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import ConfirmationCode, User
from lotracker.utils.helpers import integers_only
from lotracker.utils.serializers import ValidatorSerializer


class SignInSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        user = User.objects.filter(phone=integers_only(data.get('phone'))).first()
        if user:
            if not user.is_active:
                raise ValidationError({'user': _("Пользователь не активен")})

            confirmation = ConfirmationCode.objects.filter(user=user).last()
            if confirmation and confirmation.created_at + timedelta(minutes=1) >= timezone.now():
                raise ValidationError({'user': _("Повторная отправка SMS возможна через 60 секунд")})

        return data


class ConfirmationSerializer(ValidatorSerializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=20)

    def validate(self, data):
        if not ConfirmationCode.objects.verify(data.get('phone'), data.get('code')):
            raise ValidationError({'code': _("Неверный код подтверждения")})
        return data
