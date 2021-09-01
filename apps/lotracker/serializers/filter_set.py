from rest_framework import serializers

from lotracker.models import FilterSet, SiteTypes
from lotracker.utils.serializers import ValidatorSerializer
from reference.models import Region, Area, Organization, ProductCategory, Product
from reference.serializers import RegionSerializer, ProductCategorySerializer


class FilterDataSerializer(serializers.Serializer):
    regions = RegionSerializer(many=True)
    categories = ProductCategorySerializer(many=True)
    site_types = serializers.SerializerMethodField()

    def get_site_types(self, data):
        return [{'id': k, 'name': v} for k, v in SiteTypes.choices.items()]


class LotFilterValidator(ValidatorSerializer):
    q = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    hot_lots = serializers.BooleanField(required=False, allow_null=True)
    without_request = serializers.BooleanField(required=False, allow_null=True)
    term_date_from = serializers.DateField(required=False, allow_null=True)
    term_date_to = serializers.DateField(required=False, allow_null=True)
    price_from = serializers.IntegerField(required=False, allow_null=True)
    price_to = serializers.IntegerField(required=False, allow_null=True)
    region = serializers.PrimaryKeyRelatedField(required=False, queryset=Region.objects.all(), allow_null=True)
    area = serializers.PrimaryKeyRelatedField(required=False, queryset=Area.objects.all(), allow_null=True)
    organization = serializers.PrimaryKeyRelatedField(required=False, queryset=Organization.objects.all(),
                                                      allow_null=True)
    product_category = serializers.PrimaryKeyRelatedField(required=False, queryset=ProductCategory.objects.all(),
                                                          allow_null=True)
    product = serializers.PrimaryKeyRelatedField(required=False, queryset=Product.objects.all(), allow_null=True)
    site_type = serializers.IntegerField(required=False, allow_null=True)


class FilterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterSet
        fields = [
            'id', 'name', 'q', 'hot_lots', 'without_request', 'term_date_from', 'term_date_to', 'price_from',
            'price_to', 'region', 'area', 'organization', 'product_category', 'product', 'site_type'
        ]


class FilterSetListFilterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterSet
        fields = [
            'name', 'q', 'hot_lots', 'without_request', 'term_date_from', 'term_date_to', 'price_from',
            'price_to', 'region', 'area', 'organization', 'product_category', 'product', 'site_type'
        ]


class FilterSetExtraDataSerializer(serializers.ModelSerializer):
    region__name = serializers.CharField(source='region.name', read_only=True, allow_null=True)
    area__name = serializers.CharField(source='area.name', read_only=True, allow_null=True)
    organization__name = serializers.CharField(source='organization.name', read_only=True, allow_null=True)
    product_category__name = serializers.CharField(source='product_category.name', read_only=True, allow_null=True)
    product__name = serializers.CharField(source='product.name', read_only=True, allow_null=True)

    class Meta:
        model = FilterSet
        fields = ['region__name', 'area__name', 'organization__name', 'product_category__name', 'product__name']


class FilterSetListSerializer(serializers.ModelSerializer):
    filter = serializers.SerializerMethodField(read_only=True)
    lots_count = serializers.IntegerField(read_only=True)
    extra = serializers.SerializerMethodField(read_only=True)

    def get_filter(self, filter_set):
        return FilterSetListFilterDataSerializer(filter_set).data

    def get_extra(self, filter_set):
        return FilterSetExtraDataSerializer(filter_set).data

    class Meta:
        model = FilterSet
        fields = ['id', 'filter', 'lots_count', 'extra']
