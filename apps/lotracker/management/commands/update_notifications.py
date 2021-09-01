from django.core.management import base
from django.conf import settings

from lotracker.models import FilterSetLot, FilterSet, LotFts


class SearchUpdates(object):
    def __init__(self):
        self.filter = None
        self.latest_id = None
        self.notifications = {}

    def run(self):
        for self.filter in FilterSet.objects.all():
            self.load_latest_id()
            self.do_search()
            self.send_telegram_notifications()
        self.send_notifications()

    def save_filter_lot_without_notifications(self, pk):
        self.filter = FilterSet.objects.get(pk=pk)
        self.load_latest_id()
        self.do_search()

    def load_latest_id(self):
        obj = FilterSetLot.objects.filter(
            filter_set=self.filter,
            user=self.filter.user).order_by('-id').first()
        self.latest_id = obj.lot_id if obj else None

    def do_search(self):
        search_results = LotFts.objects.search(**self.get_filters())
        search_results and self.append_notification()
        lots = []
        for lot_id in search_results:
            lots.append(FilterSetLot(
                user_id=self.filter.user_id,
                filter_set_id=self.filter.pk,
                lot_id=lot_id
            ))
        FilterSetLot.objects.bulk_create(lots)

    def get_filters(self):
        filters = self.filter.filters.copy()
        if self.latest_id is not None:
            filters['pk_gt'] = self.latest_id
        return filters

    def append_notification(self):
        if self.filter.user_id not in self.notifications:
            self.notifications[self.filter.user_id] = [self.filter.pk]
        elif self.filter.pk not in self.notifications[self.filter.user_id]:
            self.notifications[self.filter.user_id].append(self.filter.pk)

    def send_notifications(self):
        from lotracker.tasks import device_notifications

        if settings.DEBUG is True:
            device_notifications(self.notifications)
        else:
            device_notifications.delay(self.notifications)

    def send_telegram_notifications(self):
        from lotracker.tasks import telegram_notifications

        if settings.DEBUG is True:
            telegram_notifications(self.latest_id, self.filter.pk)
        else:
            telegram_notifications.delay(self.latest_id, self.filter.pk)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        SearchUpdates().run()
