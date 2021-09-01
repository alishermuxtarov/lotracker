from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext as _

from lotracker.utils.models import BaseModel
from notifier.querysets.notification import NotificationQuerySet


class Notification(BaseModel):
    LEVELS = (
        ('success', _('Success')),
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
    )
    VERBS = (
        ('new_lot_by_filter_set', _('Новый лот по набору фильтров')),
    )

    text = models.TextField(blank=True, null=True, verbose_name=_('Текст'))
    level = models.CharField(choices=LEVELS, default='info', max_length=20)
    verb = models.CharField(max_length=100, choices=VERBS, verbose_name=_('Действие'))
    initiator = models.ForeignKey('authentication.User', CASCADE, null=True, blank=True, verbose_name=_('Инициатор'))
    recipient = models.ForeignKey('authentication.User', CASCADE, related_name='notifications',
                                  verbose_name=_('Получатель'))
    action_object_content_type = models.ForeignKey(
        ContentType, blank=True, null=True,
        related_name='notify_action_object', on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано?'))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Прочитано в'))
    data = models.TextField(null=True)

    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        return self.text or 'n/a'

    class Meta:
        db_table = 'notification_notifications'
        ordering = ('-created_at',)
        verbose_name = _('Оповещение')
        verbose_name_plural = _('Оповещения')
