from json import dumps

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from lotracker import models


@receiver(post_delete, sender=models.Lot)
def lot_post_delete(sender, instance, **kwargs):
    models.LotFts.objects.delete_record(instance.id)


@receiver(post_save, sender=models.FilterSet)
def filter_set_post_save(sender, instance, created, **kwargs):
    from lotracker.management.commands.update_notifications import SearchUpdates

    if kwargs.get('update_fields') is not None:
        return

    filters = {}
    if instance.q:
        filters['word'] = instance.q
    if instance.region_id:
        filters['region_id'] = instance.region_id
    if instance.area_id:
        filters['area_id'] = instance.area_id
    if instance.organization_id:
        filters['organization_id'] = instance.organization_id
    if instance.product_category_id:
        filters['product_category_id'] = instance.product_category_id
    if instance.product_id:
        filters['product_id'] = instance.product_id
    if instance.term_date_from:
        filters['term_date_from'] = instance.term_date_from.timestamp()
    if instance.term_date_to:
        filters['term_date_to'] = instance.term_date_to.timestamp()
    if instance.price_from:
        filters['price_from'] = instance.price_from
    if instance.price_to:
        filters['price_to'] = instance.price_to
    if instance.site_type:
        filters['site_type'] = instance.site_type
    instance.params = dumps(filters)
    instance.save(update_fields=['params'])

    SearchUpdates().save_filter_lot_without_notifications(instance.pk)
