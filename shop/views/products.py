from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.products import Product
from shop.serializers.products import ProductListSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductListSerializer
    lookup_field = 'id'

    def get_object(self):
        product_id = self.kwargs.get('id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Продукт не найден!")
        return product

    def destroy(self, request, *args, **kwargs):
        obj = Product.objects.filter(id=self.kwargs.get('id'))
        if obj:
            self.perform_destroy(obj)
            return Response({"message": "Продукт удалён!"}, status=status.HTTP_200_OK)
        return Response({"message": "Продукт не найден!"}, status=status.HTTP_404_NOT_FOUND)