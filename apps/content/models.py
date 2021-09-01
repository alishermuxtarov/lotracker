from django.utils.translation import ugettext as _
from django.db import models

from tinymce.models import HTMLField

from content.querysets.content import ContentQuerySet
from lotracker.utils.models import BaseModel


class Content(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Заголовок'))
    slug = models.SlugField(verbose_name=_('Slug'))
    text = HTMLField(verbose_name=_('Текст'))

    objects = ContentQuerySet.as_manager()

    def __str__(self):
        return self.title or 'n/a'

    class Meta:
        db_table = 'content_contents'
        ordering = ('-created_at',)
        verbose_name = _('Контент')
        verbose_name_plural = _('Контент')
