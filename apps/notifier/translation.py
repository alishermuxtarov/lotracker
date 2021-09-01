from modeltranslation.translator import register, TranslationOptions

from notifier.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('text',)
