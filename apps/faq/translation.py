from modeltranslation.translator import register, TranslationOptions

from faq.models import Faq


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
