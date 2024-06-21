from django.urls import path

from shop.views.attributes import ProductAttributeView, ProductAttributeUpdateDeleteView
from shop.views.categories import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView
from shop.views.colors import ProductColorListCreateAPIView, ProductColorUpdateDeleteAPIView
from shop.views.images import ProductImageListCreateView, ProductImageGetUpdateDeleteView
from shop.views.products import ProductListCreateView, ProductGetUpdateDeleteView
from shop.views.reviews import ReviewsListCreateAPIView, ReviewUpdateDeleteAPIView, CommentListCreateAPIView, \
    CommentUpdateDeleteAPIView, CommentLikeAPIView
from shop.views.variations import ProductVariationsListCreateAPIView, ProductVariationsUpdateDeleteAPIView

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='categories-list-create'),
    path('categories/<int:id>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='categories-list-update'),

    # Products
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductGetUpdateDeleteView.as_view(), name='product-get-update-delete'),

    # Product Attributes
    path('products/<int:product_id>/attributes', ProductAttributeView.as_view(), name='attribute-list-create'),
    path('products/<int:product_id>/attributes/<int:attribute_id>', ProductAttributeUpdateDeleteView.as_view(),
         name='attribute-get-update-delete'),

    # Product Colors
    path('products/<int:product_id>/colors', ProductColorListCreateAPIView.as_view(), name="product-colors"),
    path('products/<int:product_id>/colors/<int:color_id>', ProductColorUpdateDeleteAPIView.as_view(),
         name="product-color-update-delete"),

    # Product Images
    path('products/<int:product_id>/images', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('products/<int:product_id>/images/<int:image_id>', ProductImageGetUpdateDeleteView.as_view(),
         name='product-image-get-update-delete'),

    # Reviews
    path('products/<int:product_id>/reviews', ReviewsListCreateAPIView.as_view(), name='product-reviews-list'),
    path('products/<int:product_id>/reviews/<int:review_id>', ReviewUpdateDeleteAPIView.as_view(),
         name='get-update-delete'),
    path('reviews/<int:review_id>/comments', CommentListCreateAPIView.as_view(),
         name='comment-list'),
    path('reviews/<int:review_id>/comments/<int:comment_id>', CommentUpdateDeleteAPIView.as_view(),
         name='comment-get-update-delete'),
    path('reviews/<int:review_id>/comments/<int:comment_id>/like', CommentLikeAPIView.as_view(), name='comment-like'),

    # Product Variations

    path('products/<int:product_id>/variations', ProductVariationsListCreateAPIView.as_view(),
         name='product-variations-list-create'),
    path('products/<int:product_id>/variations/<int:variation_id>', ProductVariationsUpdateDeleteAPIView.as_view(),
         name='product-variations-get-update-delete'),

]
