from django.core.management import base, call_command
from lotracker.models import Lot


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        ids = [1227541, 5098766]
        for pk in ids:
            lot = Lot.objects.filter(bid_id=pk)
            if lot.exists():
                lot.delete()
        call_command('aggregate')
