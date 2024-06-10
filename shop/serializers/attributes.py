from rest_framework import serializers

from shop.models.products import ProductAttribute


class ProductAttributeListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ("id", "product", "attribute_name", "attribute_value")
        read_only_fields = ("id", "product")

