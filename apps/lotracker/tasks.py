from traceback import print_exc
from time import time

from config.celery import app as celery_app
from django.conf import settings

from lotracker.utils.helpers import get_text_from_file


@celery_app.task()
def lot_post_save(pk, text='', description=''):
    from lotracker import models

    instance = models.Lot.objects.get(pk=pk)

    for f in instance.attachments.all():
        text += get_text_from_file(f.file.path)

    for s in instance.products.all():
        text += ' {}'.format(s.name)
    text += ' {}'.format(instance.category.name)

    for s in instance.lot_items.all():
        description += ' {}\n {}\n'.format(s.description, s.expense_type_text)

    models.LotFts.objects.update_record(
        id=instance.pk,
        price=instance.current_price,
        start_price=instance.start_price,
        term_date=instance.term_date.timestamp(),
        area_id=instance.area_id,
        organization_id=instance.customer_id,
        product_id=instance.products.all().first().pk,
        product_category_id=instance.category_id,
        region_id=instance.region_id,
        title=instance.name,
        site_type=instance.site_type,
        description=description,
        files=text
    )


@celery_app.task()
def telegram_notifications(latest_lot_id, filter_set_id):
    import telebot
    from lotracker.models import FilterSetLot

    results = FilterSetLot.objects.filter(
        lot_id__gt=latest_lot_id or 0, filter_set_id=filter_set_id)

    bot = telebot.TeleBot(token=settings.TOKEN)

    for row in results:
        try:
            bot.send_message(
                row.user.telegram_uid, '''Найдено совпадение по фильтру: {}. 
Посмотреть лот можно по ссылке: {}'''.format(row.filter_set.name, row.lot.url))
        except telebot.apihelper.ApiException:
            # todo: check to 403, Forbidden: bot was blocked by the user
            pass


@celery_app.task()
def device_notifications(notifications):
    from fcm_django.models import FCMDevice
    from lotracker.models import FilterSet

    for user_id, filters in notifications.items():
        names = ', '.join(FilterSet.objects.values_list(
            'name', flat=True).filter(pk__in=filters))
        try:
            devices = FCMDevice.objects.filter(user_id=user_id)
            devices.send_message(
                'Найдены новые лоты',
                'По фильтру(ам) {} появились новые лоты'.format(names),
                data={'time': time(), 'type': 'new_lots_in_filter_set'}
            )
        except:
            print_exc()
