from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.categories import Category
from shop.serializers.categories import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        qs = Category.objects.filter(id=self.kwargs.get('id'))
        return qs

    def destroy(self, request, *args, **kwargs):
        obj = Category.objects.filter(id=self.kwargs.get('id'))
        if obj:
            self.perform_destroy(obj)
            return Response({"message": "Категория успешно удален!"}, status=status.HTTP_200_OK)
        return Response({"message": "Категория не найден!"}, status=status.HTTP_404_NOT_FOUND)
