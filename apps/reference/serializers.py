from rest_framework import serializers

from reference.models import Area, Region, Product, ProductCategory, Organization


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'areas']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'products']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'inn', 'address', 'phones', 'bank_account']
