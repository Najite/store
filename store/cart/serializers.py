from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Cart, CartItem
from products.serializers import ProductListSerializer
from products.models import Product

class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image',
        ]



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price', ]
        read_only_fields = ['total_price', 'cart']
        depth = 1
        


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_status', 'creation_date', 
        'modification_date', 'total_price',
        'cartitems',  
        ]
        read_only_fields = fields = ['id', 'user', 'cart_status', 'creation_date', 
        'modification_date', 'total_price',
        'cartitems', 
        ] 
    



