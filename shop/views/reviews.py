from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from shop.models.products import Product
from shop.models.reviews import Review, Comment
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
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product, author=self.request.user)


class ReviewUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewListSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        review_id = self.kwargs.get('review_id')
        qs = Review.objects.filter(product_id=product_id, id=review_id)
        return qs


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
        review = Review.objects.get(id=review_id)
        serializer.save(review=review, author=self.request.user)


class CommentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentListSerializer
    lookup_field = 'review_id'

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comment_id = self.kwargs.get('comment_id')
        qs = Comment.objects.filter(review_id=review_id, id=comment_id)
        return qs


class CommentLikeAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer
    lookup_field = 'review_id'

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        # Проверяем, есть ли уже лайк от текущего пользователя
        if CommentLike.objects.filter(comment=comment, author=self.request.user).exists():
            raise ValidationError("You have already liked this comment.")

        # Сохраняем лайк и увеличиваем счетчик лайков у комментария
        comment.helpful_votes += 1
        comment.save()
        serializer.save(author=self.request.user, comment=comment)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        comment_id = self.kwargs.get('comment_id')
        review = Review.objects.get(id=review_id)
        comment = Comment.objects.get(id=comment_id)
        comment.helpful_votes += 1
        serializer.save(author=self.request.user, review=review)
