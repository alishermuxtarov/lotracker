from modeltranslation.translator import register, TranslationOptions

from content.models import Content


@register(Content)
class ContentTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
