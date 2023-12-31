from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from products.models import Product


class CartView(ModelViewSet):
    queryset = CartItem.objects.all() 
    serializer_class = CartItemSerializer     
        

    # # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer  
    # def get_queryset(self): 
    #     if self.action == 'list' and self.action == 'retrieve':
    #         return Cart.objects.filter(user=self.request.user)
    #     else:
    #         return CartItem.objects.filter(
    #             cart__user=self.request.user
    #         ) 
        
    # def get_serialzer_class(self):
    #     if self.action == 'list' and self.action == 'retrieve':
    #         return CartSerializer
    #     else:
    #         return CartItemSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer, CartItemSerializer):
            self.perform_create_cart_item(serializer)
        else:
            self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED,
                        headers=headers
                        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_create_cart_item(self, serializer):
        cart = Cart.objects.get_or_create(
            user=self.request.user,
            cart_status='Open'
        ) [0]
        serializer.save(cart=cart)
        cart.update_total_price()
