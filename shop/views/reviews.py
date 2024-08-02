from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models.products import Product
from shop.models.reviews import Review, Comment, CommentLikeDislike
from shop.serializers.reviews import ReviewListSerializer, ReviewCreateSerializer, CommentListSerializer, \
    CommentCreateSerializer, CommentLikeSerializer


class ReviewsListCreateAPIView(ListCreateAPIView):

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')

        qs = Review.objects.filter(product_id=product_id).all()
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewListSerializer
        return ReviewCreateSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("отзывы могут оставить те пользователи которые приобрели данный товар")
        product_id = self.kwargs.get('product_id')
        if self.request.user.is_authenticated:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise ValidationError({'product': 'Неверный ID продукта.'})
            try:
                serializer.save(product=product, author=self.request.user)
            except IntegrityError:
                raise ValidationError({"reviews": "Вы уже оставили отзыв!"})
        else:
            raise ValidationError({"detail": "Authentication credentials were not provided."})


class ReviewUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewCreateSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        review_id = self.kwargs.get('review_id')
        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"products": "Неверный ID продукта."})
        qs = Review.objects.filter(product_id=product_id, id=review_id)
        if not qs:
            raise ValidationError({"reviews": "нет отзыва!"})
        return qs

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.author:
            raise ValidationError("Вы не являетесь автором данного отзыва!")
        serializer.save()

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError("Вам не разрешено удалять отзывы!")
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Отзыв продукта успешно удален!.'}, status=status.HTTP_200_OK)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        qs = Comment.objects.filter(review_id=review_id).all()
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        if self.request.user.is_authenticated:
            serializer.save(review=review, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError({"detail": "Authentication credentials were not provided."})


class CommentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentCreateSerializer
    lookup_field = 'review_id'

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comment_id = self.kwargs.get('comment_id')
        qs = Comment.objects.filter(review_id=review_id, id=comment_id)
        return qs

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.author:
            raise ValidationError("Вы не являетесь автором данной комментарии!")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise ValidationError("Вам не разрешено удалять комментарии!")

        obj = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        self.perform_destroy(obj)
        return Response({"message": "Комментарии удалён!"}, status=status.HTTP_200_OK)


class CommentLikeDislikeAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        value = serializer.validated_data['value']
        comment = get_object_or_404(Comment, pk=comment_id)
        user = self.request.user

        # Проверка на существование лайка/дизлайка от текущего пользователя
        existing_vote = CommentLikeDislike.objects.filter(comment=comment, author=user).first()

        if existing_vote:
            if existing_vote.value == value:
                raise ValidationError("Вы уже поставили такую оценку этому комментарию.")
            else:
                # Удаляем старый голос и обновляем счетчики
                if existing_vote.value == 1:
                    comment.helpful_votes -= 1
                else:
                    comment.unhelpful_votes -= 1
                existing_vote.delete()

        # Сохраняем новый голос и обновляем счетчики
        if value == 1:
            comment.helpful_votes += 1
        else:
            comment.unhelpful_votes += 1

        comment.save()
        serializer.save(author=user, comment=comment)
