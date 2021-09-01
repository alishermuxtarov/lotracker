from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import QuerySet, OuterRef, Subquery, Exists, Value, IntegerField
from django.utils.timezone import now


class LotQuerySet(QuerySet):
    def active(self):
        return self.filter(term_date__gte=datetime.now()).select_related('region', 'area', 'category', 'customer')

    def list(self, filters):
        from lotracker.models import LotFts
        qs = self.active().order_by('term_date')
        hot_lots = filters.pop('hot_lots', None)
        without_request = filters.pop('without_request', None)
        product = filters.pop('product', None)
        price_from = filters.pop('price_from', None)
        price_to = filters.pop('price_to', None)

        if hot_lots:
            qs = qs.filter(requests_count=0, term_date__lte=datetime.now() + timedelta(days=2)).filter(
                term_date__gte=datetime.now()
            )

        if without_request:
            qs = qs.filter(requests_count=0)

        if product:
            qs = qs.filter(lot_items__product=product)

        if price_from:
            qs = qs.extra(where=[
                """
                coalesce(
                  (CASE 
                    WHEN "lotracker_lots"."current_price" = 0.0 
                    THEN null 
                    ELSE "lotracker_lots"."current_price" 
                  END), 
                  "lotracker_lots"."start_price"
                ) >= %d
                """ % price_from
            ])

        if price_to:
            qs = qs.extra(where=[
                """
                coalesce(
                  (CASE 
                    WHEN "lotracker_lots"."current_price" = 0.0 
                    THEN null 
                    ELSE "lotracker_lots"."current_price" 
                  END), 
                  "lotracker_lots"."start_price"
                ) <= %d
                """ % price_to
            ])

        if 'q' in filters.keys():
            if filters.get('q') != '':
                filters['word'] = filters.pop('q')
            else:
                del filters['q']

        if len(filters) > 0:
            qs = qs.filter(pk__in=LotFts.objects.search(**filters))

        return qs

    def annotate_is_favourite(self, user):
        if user.is_authenticated:
            return self.annotate(is_favourite=Exists(user.favourite_lots.filter(pk=OuterRef('pk'))))
        return self.annotate(is_favourite=Value(None, output_field=IntegerField()))

    def aggregate(self, data):
        pass

    def get_expired_lots(self):
        return self.filter(term_date__lt=now(), is_expired=False)

    def update_expired_lots(self):
        self.get_expired_lots().update(is_expired=True)

    def bid_exists(self, external_id):
        return self.model.objects.filter(external_id=external_id).exists()

    def bid_update_requests(self, external_id, requests_count):
        return self.model.objects.filter(external_id=external_id).update(requests_count=requests_count)

    def bid_create(self, sub_ref, **kwargs):
        from lotracker.tasks import lot_post_save
        from reference.models import Product

        kwargs['term_date'] = datetime.strptime(kwargs['term_date'], '%d.%m.%Y %H:%M:%S')
        kwargs['start_price'] = kwargs['start_price'][:-3].replace(' ', '')
        attachments = kwargs.pop('attachments', None) or []
        products = kwargs.pop('products', [])
        items = kwargs.pop('items', [])

        obj = self.model.objects.create(**kwargs)

        for p in products:
            if p not in sub_ref:
                so = Product.objects.create(name=p, category_id=kwargs['category_id'])
                sub_ref[so.name] = so.pk
            obj.products.add(sub_ref[p])
        obj.save()

        for f in attachments:
            ff = obj.attachments.create()
            ff.file = f
            ff.save()

        for item in items:
            obj.lot_items.create(**item)

        if settings.DEBUG is True:
            lot_post_save(obj.pk)
        else:
            lot_post_save.delay(obj.pk)

        return obj
