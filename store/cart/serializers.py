from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Cart, CartItem
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


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_id',
            'quantity',
        ]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is not product associated with that id")
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        # request = self.context['request']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']     

        try:
            cartitem = CartItem.objects.get(product_id=product_id,
                             cart_id=cart_id
                                            )
            cartitem.quantity = quantity
            cartitem.save()

            self.instance = cartitem
            
        except:
            self.instance = CartItem.objects.create(
                product_id=product_id,
                cart_id=cart_id,
                quantity=quantity
            )
        return self.instance

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price', ]
        read_only_fields = ['total_price', 'cart']
        


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_status', 'creation_date', 
        'modification_date', 'total_price',
        'cartitems',  
        ]
        read_only_fields = [
            'id', 'user', 'cart_status', 'creation_date', 
        'modification_date', 'total_price'
        ]

            



