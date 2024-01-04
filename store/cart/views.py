from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from .models import Cart, CartItem
from .serializers import (CartSerializer,
                           CartItemSerializer,
                           AddToCartSerializer
)
from rest_framework.decorators import action
from products.models import Product
from orders.models import Order, OrderItem


class CartView(ModelViewSet):
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer

    # serializer_class = CartSerializer    
    # def get_queryset(self):
    #     return Cart.objects.filter(
    #         cart_id=self.kwargs['cart_pk']
    #     )   

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return AddToCartSerializer
    #     return CartSerializer  
    
    # def get_serializer_context(self):
    #     if self.request.method == 'POST':
    #         return {
    #         'cart_id': self.kwargs['cart_pk']
    #         }

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

    
    # def get_queryset(self):
    #     if self.action == 'retrieve':
    #         Cart.objects.all()
    #     # return super().get_queryset()
        
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return CartItemSerializer
    #     return super().get_serializer_class() 
       
    def perform_create_cart_item(self, serializer):
        cart = Cart.objects.get_or_create(
            user=self.request.user,
            cart_status='Open'
        ) [0]

        serializer.save(cart=cart)
        cart.update_total_price()




class CartItemView(ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer, AddToCartSerializer):
            create_order = self.perform_create_order(serializer)
            success_message = "success"
        else:
            success_message = 'failed'
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": success_message,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
            
    def get_queryset(self):
        return CartItem.objects.filter(
            cart_id=self.kwargs['cart_pk']
        )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }
    
    
    def perform_create_order(self, serializer):
        open_order = Order.objects.filter(
            user=self.request.user,
            order_status='Pending'
        )

        if open_order.exists():
            order = open_order.first()
        else:
            order = Order.objects.create(user=self.request.user)
            
        
        for cart_item in CartItem.objects.all():
            product = cart_item.product
            order_item = OrderItem.objects.create(
                order=order,
                product = product
            )
            
            order_item.quantity = cart_item.quantity
            order_item.total_price = cart_item.total_price
            order_item.save()
        order.save() 
        serializer.save(order=order)




