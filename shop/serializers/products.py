from rest_framework import serializers

from shop.models.products import Product, ProductImage
from shop.serializers.attributes import ProductAttributeListCreateSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "product", "image_url")

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeListCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "price", "images", "quantity", "category", "attributes")
