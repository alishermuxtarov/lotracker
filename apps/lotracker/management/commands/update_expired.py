from django.core.management import base
from lotracker.models import Lot, LotFts, FilterSetLot


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        for lot in Lot.objects.get_expired_lots():
            LotFts.objects.delete_record(lot.id)
            print(lot)
        Lot.objects.update_expired_lots()
        FilterSetLot.objects.filter(lot__is_expired=True).delete()
