from rest_framework import serializers

from shop.models.reviews import Review, Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "review", "author", "text", "created_at", "updated_at", "helpful_votes", "unhelpful_votes")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "review", "author", "text", "created_at", "updated_at", "helpful_votes", "unhelpful_votes")
        read_only_fields = ("id", "review", "author", "created_at", "updated_at", "helpful_votes", "unhelpful_votes")


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "review", "author", "text", "created_at", "updated_at", "helpful_votes", "unhelpful_votes")
        read_only_fields = (
            "id", "review", "author", "text", "created_at", "updated_at", "helpful_votes", "unhelpful_votes"
        )


class CommentDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "review", "author", "text", "created_at", "updated_at", "unhelpful_votes")
        read_only_fields = ("id", "review", "author", "text", "created_at", "updated_at", "helpful_votes")


class ReviewListSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = (
            "id", "product", "author", "text", "rating", "comments", "created_at", "updated_at", "helpful_votes",
            "unhelpful_votes"
        )


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id", "product", "author", "text", "rating", "created_at", "updated_at", "helpful_votes", "unhelpful_votes"
        )

        read_only_fields = (
            "id", "product", "author", "created_at", "updated_at", "helpful_votes", "unhelpful_votes"
        )
