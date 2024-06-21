from rest_framework import serializers

from shop.models.products import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "product", "image_url")

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class ProductImageCreateSerializer(ProductImageSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ("image", )
