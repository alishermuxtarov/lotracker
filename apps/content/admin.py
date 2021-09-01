from django.contrib import admin

from content import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['id']
