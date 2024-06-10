from rest_framework.generics import ListCreateAPIView

from shop.models.categories import Category
from shop.serializers.categories import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
