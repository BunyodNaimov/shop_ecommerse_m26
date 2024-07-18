from django.db import IntegrityError
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
        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})
        qs = ProductColor.objects.filter(product_id=product_id)
        if not qs:
            raise ValidationError({"colors": "цветов продукта не найден"})
        return qs

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут создавать цвет продукта.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})
        try:
            serializer.save(product=product)
        except IntegrityError:
            raise ValidationError({"colors": "цвет продукта уже существует!"})


class ProductColorUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductColorSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        color_id = self.kwargs.get('color_id')

        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Неверный ID продукта.'})
        qs = ProductColor.objects.filter(product_id=product_id, id=color_id)
        if not qs:
            raise ValidationError({"colors": "цвет продукта не найден"})
        return qs

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут изменить цвет продукта.')
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({"colors": "цвет продукта уже существует!"})

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут удалить цвет продукта.')
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Цвета продукта успешно удален!.'}, status=status.HTTP_200_OK)
