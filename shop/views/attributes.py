from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from shop.models.products import ProductAttribute, Product
from shop.serializers.attributes import ProductAttributeListCreateSerializer


class ProductAttributeView(ListCreateAPIView):
    serializer_class = ProductAttributeListCreateSerializer

    def get_queryset(self, *args, **kwargs):
        qs = ProductAttribute.objects.filter(product=self.kwargs['product_id']).all()
        return qs

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Проверка существования продукта перед сохранением атрибута
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})

        # Сохранение атрибута, связанного с проверенным продуктом
        try:
            serializer.save(product=product)
        except IntegrityError:
            raise ValidationError("Этот аттрибут уже есть!")


class ProductAttributeUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductAttributeListCreateSerializer
    lookup_field = 'product_id'

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        attribute_id = self.kwargs.get('attribute_id')
        qs = ProductAttribute.objects.filter(product_id=product_id, pk=attribute_id)
        return qs if qs else None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Атрибут продукта успешно удален.'}, status=status.HTTP_200_OK)
