from django.contrib import admin

from faq import models


@admin.register(models.Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'id']
    search_fields = ['question', 'answer']
    ordering = ['id']
