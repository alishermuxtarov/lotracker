from rest_framework import serializers

from lotracker.models import Lot
from lotracker.serializers.lot import LotListSerializer
from reference.models import Organization


class OrganizationDetailSerializer(serializers.ModelSerializer):
    lots = serializers.SerializerMethodField(read_only=True)

    def get_lots(self, organization):
        user = self.context.get('request').user
        lots = Lot.objects.active().filter(customer=organization).annotate_is_favourite(user)
        return LotListSerializer(lots, many=True).data

    class Meta:
        model = Organization
        fields = ['id', 'name', 'inn', 'address', 'phones', 'bank_account', 'lots']
