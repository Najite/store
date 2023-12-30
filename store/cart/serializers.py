from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Cart, CartItem
from products.serializers import ProductListSerializer



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price']
        read_only_fields = ['total_price', 'cart']

class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_status', 'creation_date', 
        'modification_date', 'total_price',
        'cartitems'
        ]



