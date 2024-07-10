from rest_framework import serializers

from shop.models.reviews import Review, Comment, CommentLikeDislike


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
    value = serializers.ChoiceField(choices=((1, "Like"), (-1, "Dislike")), required=True)

    class Meta:
        model = CommentLikeDislike
        fields = ("id", "author", "value", "created_at", "updated_at",)
        read_only_fields = (
            "id", "author", "created_at", "updated_at"
        )


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
