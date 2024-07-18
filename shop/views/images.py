from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.products import Product, ProductImage
from shop.serializers.images import ProductImageSerializer, ProductImageCreateSerializer


class ProductImageListCreateView(ListCreateAPIView):
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
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут добавить изображение продукта.')
        product_id = self.kwargs.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"products": "Продукт не найден!"})
        serializer.save(product=product)


class ProductImageGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    lookup_field = "product_id"

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductImageSerializer
        return ProductImageCreateSerializer

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        image_id = self.kwargs.get("image_id")
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"product": "Неверный ID продукта."})
        qs = ProductImage.objects.filter(product_id=product_id, pk=image_id)
        if not qs:
            raise ValidationError({"images": "Изображения не найдено"})
        return qs

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут изменить изображение продукта.')
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут удалить изображение продукта.')
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"delete": "Изображение успешно удалено!"}, status=status.HTTP_200_OK)
