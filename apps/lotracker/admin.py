from django.contrib import admin

from lotracker import models


class LotAttachmentInline(admin.TabularInline):
    model = models.LotAttachment
    extra = 0


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'external_id', 'region', 'area', 'current_price', 'term_date']
    search_fields = ['conditions', 'name', 'external_id']
    list_filter = ['category', 'region', 'area']
    inlines = [LotAttachmentInline]


@admin.register(models.FilterSet)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'q']
    search_fields = [
        'user', 'name', 'q', 'organization', ('hot_lots', 'without_request'), ('region', 'area'),
        ('product_category', 'product'), ('price_from', 'price_to'), ('term_date_from', 'term_date_to')
    ]
