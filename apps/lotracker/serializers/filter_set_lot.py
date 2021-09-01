from rest_framework import serializers

from lotracker.models import FilterSetLot
from lotracker.serializers.lot import LotListSerializer


class FilterSetLotSerializer(serializers.ModelSerializer):
    filter_set__name = serializers.CharField(source='filter_set.name', read_only=True)
    lot = LotListSerializer(read_only=True)

    class Meta:
        model = FilterSetLot
        fields = ['id', 'filter_set__name', 'lot', 'is_read']
