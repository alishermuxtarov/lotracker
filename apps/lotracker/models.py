from json import loads

from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext as _

from lotracker.querysets.fts import FTSManager
from lotracker.utils.models import BaseModel
from lotracker.querysets.lot import LotQuerySet


class SiteTypes:
    DXARID = 0
    EXARID = 1

    choices = {
        DXARID: 'dxarid',
        EXARID: 'exarid',
    }


class Lot(BaseModel):
    external_id = models.PositiveIntegerField(_('Номер лота'), db_index=True)
    name = models.TextField(_('Наименование заказа'))
    category = models.ForeignKey('reference.ProductCategory', null=True, verbose_name='Категория',
                                 on_delete=models.CASCADE)
    products = models.ManyToManyField('reference.Product', blank=True, verbose_name=_('Список товаров'))
    customer = models.ForeignKey('reference.Organization', models.CASCADE, 'lots', verbose_name=_('Заказчик'))
    region = models.ForeignKey('reference.Region', on_delete=models.CASCADE, verbose_name=_('Регион'))
    area = models.ForeignKey('reference.Area', on_delete=models.CASCADE, verbose_name=_('Город/Район'))
    start_price = models.FloatField(_('Стартовая стоимость'))
    current_price = models.FloatField(_('Текущая стоимость'), null=True)
    # todo: пока не знаю откуда брать этот показатель
    next_price = models.FloatField(_('Лучшая стоимость'), null=True)
    deposit_amount = models.FloatField(_('Залог (на следующую цену)'))
    commission_amount = models.FloatField(_('Сумма комиссионного сбора (на следующую цену)'))
    delivery_days_count = models.PositiveIntegerField(_('Срок поставки(рабочих дней)'))
    payment_days_count = models.PositiveIntegerField(_('Срок оплаты'))
    need_delivery = models.BooleanField(_('Продавец осуществляет доставку'), default=True)
    delivery_address = models.CharField(_('Адрес доставки'), max_length=255)
    term_date = models.DateTimeField(_('Срок окончания торгов'))
    conditions = models.TextField(_('Условия'))
    url = models.URLField(_('URL источника'), unique=True, max_length=150)
    requests_count = models.PositiveSmallIntegerField(_('Кол-во заявок'))
    site_type = models.SmallIntegerField(
        choices=SiteTypes.choices.items(), default=SiteTypes.EXARID, db_index=True)
    is_expired = models.BooleanField(default=False, db_index=True)

    objects = LotQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.external_id, self.name)

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Лот')
        verbose_name_plural = _('Лоты')
        index_together = (('term_date', 'is_expired'),)
        db_table = 'lotracker_lots'


class LotItem(BaseModel):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='lot_items')
    product = models.ForeignKey('reference.Product', on_delete=models.CASCADE, related_name='lot_items')
    description = models.TextField(_('Подробное описание'))
    expense_type_text = models.TextField(_('Статья расходов'))
    quantity = models.FloatField(_('Количество товара'))
    unit = models.CharField(_('Единица измерения'), max_length=20)
    start_price = models.FloatField(_('Стартовая стоимость'))
    current_price = models.FloatField(_('Текущая стоимость'), null=True)
    next_price = models.FloatField(_('Лучшая стоимость'), null=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['pk']
        verbose_name = _('Элементы лота')
        verbose_name_plural = _('Элементы лота')
        db_table = 'lotracker_lot_items'


class LotAttachment(BaseModel):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments')

    # todo: add TEXT Version

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлы')
        db_table = 'lotracker_lot_attachments'


class FilterSet(BaseModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    name = models.CharField('Наименование фильтра', max_length=255)
    q = models.CharField('Поисковое слово', max_length=255, null=True)
    hot_lots = models.BooleanField(_('Горящие лоты'), null=True)
    without_request = models.BooleanField(_('Без заявок'), null=True)
    term_date_from = models.DateTimeField(_('Срок окончания торгов (от)'), null=True)
    term_date_to = models.DateTimeField(_('Срок окончания торгов (до)'), null=True)
    price_from = models.BigIntegerField(_('Стоимость (от)'), null=True)
    price_to = models.BigIntegerField(_('Стоимость (до)'), null=True)
    region = models.ForeignKey('reference.Region', CASCADE, null=True, verbose_name=_('Регион'))
    area = models.ForeignKey('reference.Area', CASCADE, null=True, verbose_name=_('Город/Район'))
    organization = models.ForeignKey('reference.Organization', CASCADE, null=True, verbose_name=_('Организация'))
    product_category = models.ForeignKey('reference.ProductCategory', CASCADE, null=True,
                                         verbose_name=_('Категория товаров'))
    product = models.ForeignKey('reference.Product', CASCADE, null=True, verbose_name=_('Товар'))
    site_type = models.SmallIntegerField(_('Сайт'), choices=SiteTypes.choices.items(), null=True)
    params = models.TextField(null=True, blank=True, editable=False)

    @property
    def filters(self):
        if self.params:
            return loads(self.params)
        return {}

    class Meta:
        ordering = ['-pk']
        verbose_name = "Сохраненный набор фильтров"
        verbose_name_plural = "Сохраненные наборы фильтров"
        db_table = 'lotracker_filter_sets'


class FilterSetLot(models.Model):
    user = models.ForeignKey('authentication.User', models.CASCADE, 'filter_sets_lots', verbose_name=_('Пользователь'))
    filter_set = models.ForeignKey(FilterSet, models.CASCADE, 'lots', verbose_name=_('Сохраненный набор фильтров'))
    lot = models.ForeignKey(Lot, models.CASCADE, 'filter_sets_lots', verbose_name=_('Лот'))
    is_read = models.BooleanField(_('Прочитано?'), default=False)
    is_displayed = models.BooleanField(_('Отображено?'), default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name=_('Время создания'))

    class Meta:
        ordering = ['-pk']
        verbose_name = "Найденные лоты сохраненных фильтров"
        verbose_name_plural = "Найденные лоты сохраненных фильтров"
        db_table = 'lotracker_filter_sets_lots'


class LotFts(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.FloatField(default=0)
    start_price = models.FloatField(default=0)
    term_date = models.IntegerField(default=0)
    area_id = models.IntegerField(default=0)
    organization_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)
    product_category_id = models.IntegerField(default=0)
    region_id = models.IntegerField(default=0)
    site_type = models.IntegerField(default=0)
    title = models.TextField(default='')
    files = models.TextField(default='')
    description = models.TextField(default='')

    objects = FTSManager()

    class Meta:
        managed = False
        db_table = 'lots'
