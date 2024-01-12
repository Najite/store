from rest_framework.viewsets import ModelViewSet
from .serialzers import ( 
    OrderItemSerializer,
    OrderSerializer,
    CreateOrderSerializer
)

from .models import Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
import requests


def initiate_payment(amount, email, order_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"
    }
    data = {
        'tx_ref': 'rrerfe',
        'amount': str(amount),
        'currency': 'NGN',
        "redirect_url": "redirect_url",
        "customer": {
            "email": email,
            'name': "emma"
        }
    }


    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        print('Failed Payment')
        return Response(
            {
                "error": err
            
            },
            status=500
        )


class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        else:
            return super().get_serializer_class()
        
    
    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id
        }

    @action(detail=True, methods=['POST'])
    def pay(self, request, pk):
        # print('here')
        order = self.get_object()
        amount = order.total_price
        email = request.user.email
        # user = request.user
        redirect_url = 'http://127.0.0.1:8000/confirm'
        order_id = order.id
        return initiate_payment(amount, email, order_id)
    
    
    @action(detail=False, methods=["POST"])
    def confirm_payment(self, request):
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        order.order_status = "Confirmed"
        order.save()
        serializer = OrderSerializer(order)

        data = {
            "message": "Payment successful",
            "data" : serializer.data
        }
        
        Response(
            data
        )

        
