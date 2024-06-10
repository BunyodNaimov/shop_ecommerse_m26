from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from shop.models.products import ProductVariation, Product
from shop.serializers.variations import ProductVariationSerializer


class ProductVariationsListCreateAPIView(ListCreateAPIView):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer

    def get_queryset(self):
        qs = ProductVariation.objects.filter(product_id=self.kwargs.get('product_id'))
        return qs

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})
        try:
            serializer.save(product=product)
        except IntegrityError:
            raise ValidationError("Такое вариант продукта уже есть!")


class ProductVariationsUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductVariationSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        variation_id = self.kwargs.get('variation_id')
        qs = ProductVariation.objects.filter(product_id=product_id, id=variation_id)
        return qs if qs else None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Вариант продукта успешно удален.'}, status=status.HTTP_200_OK)