from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models.orders import Order, Basket, OrderItem
from shop.models.products import Product
from shop.serializers.orders import BasketCreateSerializer, BasketListSerializer, \
    OrderCreateSerializer, OrderListSerializer, OrderCancelSerializer


class AddToBasketAPIView(CreateAPIView):
    serializer_class = BasketCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=kwargs.get('product_id'))
        if product.quantity <= 0:
            return Response({"error": "Извините, товар временно недоступен"}, status=status.HTTP_400_BAD_REQUEST)
        baskets = Basket.objects.filter(author=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(author=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        return Response({"status": "Вы добавили товар в корзину"}, status=status.HTTP_201_CREATED)


class BasketListAPIView(ListAPIView):
    serializer_class = BasketListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Basket.objects.filter(author=self.request.user)
        return qs


class RemoveFromBasketAPIView(DestroyAPIView):
    serializer_class = BasketListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'product_id'

    def get_queryset(self):
        qs = Basket.objects.filter(author=self.request.user)
        return qs

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_in_basket = Basket.objects.filter(author=self.request.user, product_id=product_id).first()
        if product_in_basket is None:
            return Response({"В вашей корзине нет такого товара!"}, status=status.HTTP_404_NOT_FOUND)
        if product_in_basket.quantity > 1:
            product_in_basket.quantity -= 1
            product_in_basket.save()
            return Response({"Количество товара уменьшено"}, status=status.HTTP_201_CREATED)
        else:
            product_in_basket.delete()

        return Response({"Товар удален из вашей корзины"}, status=status.HTTP_201_CREATED)


class ListCreateOrderAPIView(ListCreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        qs = Order.objects.filter(author=self.request.user).all()
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        transaction.atomic() в Django является контекстным менеджером,
        который обеспечивает атомарность базовых операций базы данных.
        Атомарность означает, что либо все операции в транзакции будут успешно выполнены,
        либо ни одна из них не будет выполнена.
        """

        baskets = Basket.objects.filter(author=request.user)

        if not baskets.exists():
            return Response({"error": "Ваша корзина пуста. Добавьте товары перед оформлением заказа."},
                            status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in baskets)

        with transaction.atomic():
            order = Order.objects.create(
                author=request.user,
                address=request.data.get('address'),
                status='pending',
                total_price=total_price
            )

            # Сохраняем товары из корзины в OrderItem перед удалением корзины
            for item in baskets:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                # Уменьшаем количество товара в наличии
                product = Product.objects.get(pk=item.product.id)
                product.quantity -= item.quantity
                product.save()

            # Очищаем корзину после создания заказа
            baskets.delete()

        return Response({"status": "Заказ успешно создан"}, status=status.HTTP_201_CREATED)


class OrderCancelAPIView(CreateAPIView):
    serializer_class = OrderCancelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(author=request.user, id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        if order.status == 'cancelled':
            return Response({"error": "Заказ уже отменен"}, status=status.HTTP_400_BAD_REQUEST)

            # Возврат количества товаров в базу данных
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            product.quantity += order_item.quantity
            product.save()

        order.status = 'cancelled'
        order.save()

        return Response({"message": "Заказ успешно отменен"}, status=status.HTTP_200_OK)
