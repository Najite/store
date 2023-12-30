from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartView(ModelViewSet):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer  
    def get_queryset(self): 
        if self.action == 'list' and self.action == 'retrieve':
            return Cart.objects.filter(user=self.request.user)
        else:
            return CartItem.objects.filter(
                cart__user=self.request.user
            )
        
    def get_serialzer_class(self):
        if self.action == 'list' and self.action == 'retrieve':
            return CartSerializer
        else:
            return CartItemSerializer
        

    def perform_create(self, serializer):
        if isinstance(serializer, CartItemSerializer):
            cart = Cart.objects.get_or_create(
                user=self.request.user,
                cart_status='Open'
            )[0]
            serializer.save(cart=cart)
            cart.update_total_price()
        else:
            serializer.save(user=self.request.user)

