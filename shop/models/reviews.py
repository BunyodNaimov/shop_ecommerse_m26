from django.db import models


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_votes = models.IntegerField(help_text="полезный", default=0)
    unhelpful_votes = models.IntegerField(help_text="бесполезный", default=0)

    class Meta:
        unique_together = ('author', 'product')


class ReviewLikeDislike(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='review_likes')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='review_likes')
    value = models.SmallIntegerField(choices=((1, 'Like'), (-1, 'Dislike')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_votes = models.IntegerField(help_text="полезный", default=0)
    unhelpful_votes = models.IntegerField(help_text="бесполезный", default=0)


class CommentLikeDislike(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comment_likes')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='comment_likes')
    value = models.SmallIntegerField(choices=((1, 'Like'), (-1, 'Dislike')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
