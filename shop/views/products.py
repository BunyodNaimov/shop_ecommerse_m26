from rest_framework.generics import ListAPIView, ListCreateAPIView

from shop.models.products import Product, ProductImage
from shop.serializers.products import ProductListSerializer, ProductImageSerializer


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductImageView(ListAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        return ProductImage.objects.filter(product_id=product_id).all()
