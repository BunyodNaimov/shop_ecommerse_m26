from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.products import Product, ProductImage
from shop.serializers.products import ProductListSerializer, ProductImageSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductGetUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductListSerializer
    lookup_field = 'id'

    def get_queryset(self):
        qs = Product.objects.filter(id=self.kwargs.get('id'))
        return qs

    def destroy(self, request, *args, **kwargs):
        obj = Product.objects.filter(id=self.kwargs.get('id'))
        if obj:
            self.perform_destroy(obj)
            return Response({"message": "Продукт удалён!"}, status=status.HTTP_200_OK)
        return Response({"message": "Продукт не найден!"}, status=status.HTTP_404_NOT_FOUND)


class ProductImageView(ListAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        return ProductImage.objects.filter(product_id=product_id).all()
