from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management import base

from grab import Grab, GrabError

from reference.models import Region, Area, ProductCategory, Product, Organization
from lotracker.utils.helpers import md5_text
from lotracker import models


class Skip(Exception):
    pass


class Command(base.BaseCommand):
    LOT_STRUCT = [
        'term_date', 'external_id', 'region_id', 'area_id',
        'name', 'start_price', 'requests_count',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = None
        self.url = None
        self.region = {}
        self.area = {}
        self.category = {}
        self.product = {}
        self.customer = {}

    def get(self, url):
        try:
            self.g.go(url)
        except GrabError:
            try:
                self.g.go(url)
            except Exception as msg:
                raise Skip(msg)

    def load_area_and_region(self):
        for obj in Region.objects.all():
            self.region[obj.name] = obj.pk
        for obj in Area.objects.all():
            self.area[obj.name] = obj.pk
        for obj in ProductCategory.objects.all():
            self.category[obj.name] = obj.pk
        for obj in Product.objects.all():
            self.product[obj.name] = obj.pk
        for obj in Organization.objects.all():
            self.customer[obj.inn] = obj.pk

    def get_sites(self):
        e, s = date.today() + timedelta(days=60), date.today()
        e, s = e.strftime('%d.%m.%Y'), s.strftime('%d.%m.%Y')
        return {
            'https://exarid.uzex.uz/ru/ajax/filter?PageSize=1000&Src=AllMarkets&Type=trade&PageIndex=1': 'https://exarid.uzex.uz/ru/trade/lot/{}/',
            'https://dxarid.uzex.uz/ru/ajax/filter?PageSize=1000&EndDate={}&Src=AllMarkets&Type=trade&startdate={}&PageIndex=1'.format(e, s): 'https://dxarid.uzex.uz/ru/trade/lot/{}/',
        }

    def handle(self, *args, **options):
        self.load_area_and_region()
        for url, self.url in self.get_sites().items():
            try:
                self.g = Grab(timeout=25, connect_timeout=15)
                self.get(url)
                self.parse_bids()
            except Skip:
                continue

    def parse_bids(self):
        bids = self.g.doc.select('//tr')
        if bids.count() < 1:
            print('Лоты не найдены!')
            return

        print('Всего: {}'.format(bids.count()))
        for el in bids[1:]:
            try:
                self.save_bid([e.text() for e in el.select('td')[1:8]])
            except Skip:
                print('Skip')
                continue

    def save_bid(self, bid):
        if '.' in bid[1]:
            bid[0], bid[1] = bid[1], bid[0]
        data = dict(zip(self.LOT_STRUCT, bid))
        rq = data.get('requests_count') or 0
        data['requests_count'] = int(rq.split('(')[-1].rstrip(')').strip() if rq != 'Пока не подана' else 0)
        bpk = data['external_id']
        if not models.Lot.objects.bid_exists(bpk):
            data.update(self.get_bid_info(bpk))
            try:
                data['region_id'] = self.region[data['region_id']]
            except KeyError:
                self.create_region(data['region_id'])
                data['region_id'] = self.region[data['region_id']]
            try:
                data['area_id'] = self.area[data['area_id']]
            except KeyError:
                self.create_area(data['region_id'], data['area_id'])
                data['area_id'] = self.area[data['area_id']]

            data['products'] = [t.strip() for t in data['name'].split(',')]

            import pprint
            pprint.pprint(data)
            # todo: uncomment me
            models.Lot.objects.bid_create(self.product, **data)
        elif data['requests_count'] > 0:
            models.Lot.objects.bid_update_requests(bpk, data['requests_count'])

    def get_text(self, path):
        el = self.g.doc.select(path)
        if el.exists():
            return el.text().strip()
        return ''

    def get_price(self, path):
        data = self.get_text(path).rstrip('UZS').replace(' ', '')
        if data:
            return float(data)

    def get_customer(self, index):
        return self.get_text('//ul[@class="product_info"]/li[{}]/div[2]'.format(index))

    def get_bid_info(self, bid_id):
        lot_url = self.url.format(bid_id)
        self.get(lot_url)
        # info = self.g.doc.select('//ul[@class="product_info"]')
        # info = '\n'.join(e.text().strip() for e in info.select('li'))
        cond = self.g.doc.select('//ul[@class="conditionsList"]')
        cond = '\n'.join(e.text().strip() for e in cond.select('li'))
        # desc = self.g.doc.select('//div[@class="full_block content"]/p')
        # titles = self.g.doc.select('//h3[@class="min_title"]')
        cat = self.g.doc.select('//h1[@class="form_title"]/strong').text().strip()
        curr_price = self.get_text('//*[@class="lot_price"]').rstrip('UZS').replace(' ', '')
        curr_price = curr_price != 'Поканеподана' and float(curr_price)
        deposit_amount = self.get_price("//div[contains(text(), 'Залог')]/../div[2]")
        commission_amount = self.get_price("//div[contains(text(), 'Комиссионные')]/../div[2]")
        if not commission_amount:
            commission_amount = self.get_price("//div[contains(text(),'Сумма ком сбора')]/../div[2]")
        delivery_days_count = self.get_text("//div[contains(text(), 'Срок поставки')]/../div[2]").split()[0]
        payment_days_count = self.get_text("//div[contains(text(), 'Срок оплаты')]/../div[2]").split()[0]
        need_delivery = self.g.doc.select('//div[contains(text(), "Продавец осуществляет доставку")]').exists()
        customer = {
            'inn': self.get_customer(1),
            'name': self.get_customer(2),
            'address': self.get_customer(3),
            'bank_account': self.get_text("//div[contains(text(),'Лицевой счет')]/../div[2]"),
            'phones': str(
                '{}, {}'.format(
                    self.get_text("//*[contains(text(), 'Телефон:') or contains(text(), 'Телефон организации:')]/../div[2]").lstrip('(+998) '),
                    self.get_text("//*[contains(text(), 'Телефон 2:')]/../../div[2]/strong"))
            ).strip().rstrip(','),
        }
        delivery_address = customer['address']
        delivery_address_set = self.get_text('//div[contains(text(), "Адрес доставки")]/../div[2]')
        if need_delivery and delivery_address_set:
            delivery_address = delivery_address_set

        # description = ''
        # for i, title in enumerate(titles):
        #     description += '{}\n{}\n\n'.format(title.text(), desc[i].text())
        attachments = []

        for f in self.g.doc.select('//a[@class="product_file"]'):
            url = f.attr('href')
            ext = url.split('.')[-1].lower()
            self.get(url)
            filename = '{}.{}'.format(md5_text(url), ext)
            attachments.append(ContentFile(self.g.doc.body, filename))

        if cat not in self.category:
            print('Category "{}" not found'.format(cat))
            co = ProductCategory.objects.create(name=cat)
            self.category[cat] = co.pk

        if customer['inn'] not in self.customer:
            print('Organization "{}" not found'.format(cat))
            org = Organization.objects.create(**customer)
            self.customer[customer['inn']] = org.pk

        site_type = models.SiteTypes.EXARID if 'exarid.' in lot_url else models.SiteTypes.DXARID
        contents = self.g.doc.select(
            '//div[@class="full_block content"]/p/strong[contains(text(), "Подробное описание")]/../..')
        desc, arts, items = [], [], []
        desc = [c.select('p[1]').text().split(':')[1].strip() for c in contents if c.select('p[1]').exists()]
        arts = [c.select('p[2]').text().split(':')[1].strip() for c in contents if c.select('p[2]').exists()]
        head = [c.text() for c in self.g.doc.select('//div[@class="full_block content"]/../h3')]
        data = [[r.text() for r in c.select('table/tr/td')] for c in contents]

        for i, d in enumerate(data):
            cp = d[3].rstrip('UZS').replace(' ', '')
            np = d[4].rstrip('UZS').replace(' ', '')
            product = head[i].split('-')[-1].strip()
            if product not in self.product:
                print('Product "{}" not found'.format(product))
                self.create_product(product, self.category[cat])
            items.append({
                'product_id': self.product[product],
                'description': desc[i],
                'expense_type_text': arts[i] if len(arts) > i else '',
                'quantity': d[0],
                'unit': d[1],
                'start_price': d[2].rstrip('UZS').replace(' ', ''),
                'current_price': (cp != 'Поканеподана' and float(cp)) or None,
                'next_price': (np != 'Поканеподана' and float(np)) or None,
            })

        return {
            'category_id': self.category[cat],
            'conditions': cond,
            'items': items,
            'attachments': attachments,
            'current_price': curr_price,
            'deposit_amount': deposit_amount,
            'commission_amount': commission_amount,
            'url': lot_url,
            'customer_id': self.customer[customer['inn']],
            'delivery_days_count': delivery_days_count,
            'payment_days_count': payment_days_count,
            'need_delivery': need_delivery,
            'delivery_address': delivery_address,
            'site_type': site_type,
        }

    def create_region(self, name):
        obj = Region.objects.create(name=name)
        self.region[obj.name] = obj.pk
        return obj

    def create_area(self, region_id, name):
        obj = Area.objects.create(region_id=region_id, name=name)
        self.area[obj.name] = obj.pk
        return obj

    def create_product(self, name, category_id):
        obj = Product.objects.create(category_id=category_id, name=name)
        self.product[obj.name] = obj.pk
        return obj
