from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.products import ProductColor, Product
from shop.serializers.colors import ProductColorSerializer


class ProductColorListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductColorSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        qs = ProductColor.objects.filter(product_id=product_id).all()
        return qs

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)

        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})
        serializer.save(product=product)


class ProductColorUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductColorSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        color_id = self.kwargs.get('color_id')
        qs = ProductColor.objects.filter(product_id=product_id, id=color_id)
        return qs if qs else None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Цвета продукта успешно удален!.'}, status=status.HTTP_200_OK)
