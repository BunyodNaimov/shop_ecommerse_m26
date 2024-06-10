from rest_framework import serializers

from shop.models.products import ProductVariation


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ("id", "product", "variation", "price", "quantity")
        read_only_fields = ("id", "product")
