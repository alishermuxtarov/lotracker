from django.core.management import base

from lotracker.models import Lot
from lotracker.tasks import lot_post_save


class Command(base.BaseCommand):

    def handle(self, *args, **options):
        for lot in Lot.objects.all():
            lot_post_save(pk=lot.pk)
