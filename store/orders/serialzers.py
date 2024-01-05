from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from django.db import transaction
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image',
        ]



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "quantity",
            "total_price"
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_status",
            "order_date",
            "order_item"
        ]
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context['user_id']
            order = Order.objects.create(user_id=user_id)
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price
                )
            for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()
        return order
