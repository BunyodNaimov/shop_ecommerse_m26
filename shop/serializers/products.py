from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from shop.models.products import Product, ProductImage
from shop.serializers.attributes import ProductAttributeListCreateSerializer
from shop.serializers.images import ProductImageSerializer


class ProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "title", 'description', "price", "quantity", "average_rating", 'category')
        read_only_fields = ("id", "average_rating", "category")

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_average_rating(self, obj):
        return obj.average_rating()


class ProductDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeListCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "title", "slug", "description", "price", "images", "quantity", "category", "attributes",
            "average_rating"
        )
        read_only_fields = ("id", "slug", "category")

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_average_rating(self, obj):
        return obj.average_rating()
