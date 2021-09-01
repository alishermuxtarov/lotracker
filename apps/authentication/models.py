import random
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from authentication.querysets.confirmation import ConfirmationQuerySet
from authentication.querysets.users import UsersManager
from lotracker.utils.models import BaseModel


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Номер телефона'), db_index=True)
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name=_('Последняя активность'))
    favourite_lots = models.ManyToManyField('lotracker.Lot', 'favourite_of_users', verbose_name=_('Сохраненные лоты'))
    telegram_uid = models.BigIntegerField(null=True, blank=True, editable=False)

    objects = UsersManager()

    class Meta(AbstractUser.Meta):
        app_label = 'authentication'


class ConfirmationCode(BaseModel):
    AUTHENTICATION = 'authentication'
    CHANGE_PHONE = 'change_phone'

    TYPES = (
        (AUTHENTICATION, _('Авторизация')),
        (CHANGE_PHONE, _('Смена телефона'))
    )

    type = models.CharField(max_length=255, choices=TYPES, default=AUTHENTICATION)
    phone = models.CharField(max_length=20, verbose_name=_('Номер телефона'))
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_('Пользователь'))
    code = models.CharField(max_length=20, verbose_name=_('Код подтверждения'))
    is_used = models.BooleanField(default=False, verbose_name=_('Был использован?'))
    expires_at = models.DateTimeField(verbose_name=_('Срок действия'))

    objects = ConfirmationQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.code = str(random.randint(1000, 9999)) if settings.SEND_CONFIRMATION_SMS else "0000"
        self.expires_at = timezone.now() + timedelta(hours=2)
        return super().save(*args, **kwargs)

    def send(self):
        # todo: sms sending backend
        pass

    def __str__(self):
        return str(self.code) or 'n/a'

    class Meta:
        get_latest_by = 'id'
        db_table = 'authentication_confirmation_codes'
        verbose_name = _('Код подтверждения')
        verbose_name_plural = _('Коды подтверждения')


class Token(BaseModel):
    key = models.CharField(max_length=40, verbose_name=_("Ключ"), unique=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='tokens', verbose_name=_("Пользователь"))

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'authentication_tokens'
        verbose_name = _("Ключ доступа")
        verbose_name_plural = _("Ключи доступа")
