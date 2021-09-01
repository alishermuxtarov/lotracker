from django.db import models
from django.utils.translation import ugettext as _

from lotracker.utils.models import BaseModel
from reference.querysets.organization import OrganizationQuerySet


class Region(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')
        db_table = 'reference_regions'


class Area(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)
    region = models.ForeignKey(Region, models.CASCADE, 'areas', verbose_name=_('Регион'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Город/Район')
        verbose_name_plural = _('Города/Районы')
        db_table = 'reference_areas'


class ProductCategory(BaseModel):
    name = models.CharField(_('Наименование'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Категория товаров')
        verbose_name_plural = _('Категории товаров')
        db_table = 'reference_categories'


class Product(BaseModel):
    name = models.CharField(_('Наименование'), max_length=1000)
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        db_table = 'reference_products'


class Organization(BaseModel):
    name = models.CharField(_('Наименование'), max_length=500)
    inn = models.CharField(_('ИНН'), max_length=20)
    address = models.CharField(_('Адрес'), max_length=255)
    phones = models.CharField(_('Телефоны'), max_length=255)
    bank_account = models.CharField(_('Расчетный счет'), max_length=50)

    objects = OrganizationQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Организация')
        verbose_name_plural = _('Организации')
        db_table = 'reference_organizations'
