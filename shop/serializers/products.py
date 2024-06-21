from rest_framework import serializers

from shop.models.products import Product, ProductImage
from shop.serializers.attributes import ProductAttributeListCreateSerializer
from shop.serializers.images import ProductImageSerializer


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeListCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "slug", "description", "price", "images", "quantity", "category", "attributes")
        read_only_fields = ("id", "slug",)
