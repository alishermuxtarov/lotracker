from django.utils.translation import ugettext as _
from django.db import models

from tinymce.models import HTMLField

from faq.querysets.faq import FaqQuerySet
from lotracker.utils.models import BaseModel


class Faq(BaseModel):
    question = models.CharField(max_length=100, verbose_name=_('Вопрос'))
    answer = HTMLField(verbose_name=_('Ответ'))

    objects = FaqQuerySet.as_manager()

    def __str__(self):
        return self.question or 'n/a'

    class Meta:
        db_table = 'faq_faqs'
        ordering = ('-created_at',)
        verbose_name = _('Чаво')
        verbose_name_plural = _('Чаво')
