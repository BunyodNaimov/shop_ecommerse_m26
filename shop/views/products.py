from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from shop.models.categories import Category
from shop.models.products import Product
from shop.serializers.products import ProductListSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.filter(category_id=self.kwargs.get('category_id')).all()
        return qs

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут создавать продукты.')
        category = get_object_or_404(Category, pk=kwargs.get('category_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get_object(self):
        product_id = self.kwargs.get('id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Продукт не найден!")
        return product

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут изменить продукты.')
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут удалить продукты.')
        obj = Product.objects.filter(id=self.kwargs.get('id'))
        if obj:
            self.perform_destroy(obj)
            return Response({"message": "Продукт удалён!"}, status=status.HTTP_200_OK)
        return Response({"message": "Продукт не найден!"}, status=status.HTTP_404_NOT_FOUND)
