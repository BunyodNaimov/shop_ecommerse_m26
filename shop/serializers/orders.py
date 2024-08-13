from rest_framework import serializers

from shop.models.orders import Order, Basket, OrderItem
from shop.serializers.products import ProductListSerializer


class BasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ("id", "product", "author")
        read_only_fields = ("id", "product", "author")


class BasketListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Basket
        fields = ("id", "product", "quantity")
        read_only_fields = ("id",)


class OrderItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity")


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "address")
        read_only_fields = ("id",)


class OrderCancelSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Order
        fields = ("id", "author", "status", "total_price", "created_at", "updated_at")
        read_only_fields = ("id", "status", "total_price", "created_at", "updated_at")


class OrderListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "author", "status", "total_price", "created_at", "updated_at", "order_items")
        read_only_fields = ("id", "status", "total_price", "created_at", "updated_at")

    def get_order_items(self, obj):
        data = []
        for item in obj.order_items.all():
            product_data = {
                'product_id': item.product.id,
                'product_title': item.product.title,
                'quantity_ordered': item.quantity
            }
            data.append(product_data)
        return data
