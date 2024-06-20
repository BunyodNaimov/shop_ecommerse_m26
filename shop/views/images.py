from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView

from shop.models.products import Product, ProductImage
from shop.serializers.images import ProductImageSerializer, ProductImageCreateSerializer


class ProductImageView(ListCreateAPIView):
    serializer_class = ProductImageSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductImageSerializer
        return ProductImageCreateSerializer

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"products": "Продукт не найден!"})

        qs = ProductImage.objects.filter(product_id=product_id)

        if not qs:
            raise ValidationError({"images": "Изображения продукта не найдено!"})

        return qs

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"products": "Продукт не найден!"})
        serializer.save(product=product)
