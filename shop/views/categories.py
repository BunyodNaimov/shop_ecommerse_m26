from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from shop.models.categories import Category
from shop.serializers.categories import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут создавать категория.')

        serializer.save()


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        qs = Category.objects.filter(id=self.kwargs.get('id'))
        return qs

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут изменить категории.')
        serializer.save()


    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError('Только суперпользователи могут удалить категории.')
        obj = Category.objects.filter(id=self.kwargs.get('id'))
        if obj:
            self.perform_destroy(obj)
            return Response({"message": "Категория успешно удален!"}, status=status.HTTP_200_OK)
        return Response({"message": "Категория не найден!"}, status=status.HTTP_404_NOT_FOUND)
