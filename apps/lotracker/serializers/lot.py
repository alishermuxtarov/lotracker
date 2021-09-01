from rest_framework import serializers

from lotracker.models import Lot, LotItem
from reference.serializers import OrganizationSerializer


class LotItemInlineSerializer(serializers.ModelSerializer):
    product__name = serializers.CharField(source='product.name')

    class Meta:
        model = LotItem
        fields = [
            'id', 'product__name', 'description', 'expense_type_text', 'quantity', 'unit', 'start_price',
            'current_price', 'next_price'
        ]


class LotListSerializer(serializers.ModelSerializer):
    category__name = serializers.CharField(source='category.name', read_only=True)
    region__name = serializers.CharField(source='region.name', read_only=True)
    area__name = serializers.CharField(source='area.name', read_only=True)
    customer__name = serializers.CharField(source='customer.name', read_only=True)
    is_favourite = serializers.BooleanField(allow_null=True)

    class Meta:
        model = Lot
        fields = [
            'id', 'external_id', 'name', 'start_price', 'customer', 'current_price', 'next_price', 'term_date',
            'requests_count', 'site_type', 'is_expired',
            'category__name', 'region__name', 'area__name', 'customer__name', 'is_favourite'
        ]


class LotDetailSerializer(serializers.ModelSerializer):
    category__name = serializers.CharField(source='category.name', read_only=True)
    region__name = serializers.CharField(source='region.name', read_only=True)
    area__name = serializers.CharField(source='area.name', read_only=True)
    customer = OrganizationSerializer(read_only=True)
    lot_items = LotItemInlineSerializer(many=True, read_only=True)
    conditions = serializers.SerializerMethodField(read_only=True)
    is_favourite = serializers.BooleanField(allow_null=True)

    def get_conditions(self, lot):
        return lot.conditions.split('\n')

    class Meta:
        model = Lot
        fields = [
            'id', 'external_id', 'name', 'start_price', 'customer', 'current_price', 'next_price', 'deposit_amount',
            'commission_amount', 'delivery_days_count', 'payment_days_count', 'need_delivery', 'delivery_address',
            'term_date', 'conditions', 'url', 'requests_count', 'site_type', 'is_expired', 'is_favourite',
            'category__name', 'region__name', 'area__name',
            'lot_items'
        ]


class SuggestionSerializer(serializers.Serializer):
    title = serializers.CharField()
