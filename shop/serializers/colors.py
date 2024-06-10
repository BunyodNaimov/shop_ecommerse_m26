from rest_framework import serializers

from shop.models.products import ProductColor


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ("id", "product", "color", "hex_code")
        read_only_fields = ("id", "product")
