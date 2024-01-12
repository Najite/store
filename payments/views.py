from rest_framework.viewsets import ModelViewSet
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all() 
    serializer_class = PaymentSerializer

    # def create(self, request, *args, **kwargs):
    #     amount = request.data.get('amount')
    #     url = 'url'
    #     headers = {
    #         "Authorization": 'token',
    #     }
    #     response = requests.post(url, 
    #                              data={'amount':amount},
    #                              headers=headers
    #                              )
    #     payment_data = {"amount": amount, 
    #                     "reference": response.json().get(
    #                         "reference"
    #                     ),
    #                     "status": "Pending"
    #                     }
    #     serializer = PaymentSerializer(data=payment_data)
    #     if serializer.is_valid():
    #         payment_instance = serializer.save()
    #         order_data = {"field": 'field'}
    #         order_serializer = OrderSerializer(data=order_data)
    #         if order_serializer.is_valid():
    #             order_instance = order_serializer.save()
    #             payment_instance.order = order_instance
    #             payment_instance.save()
            
    #         return Response(
    #             serializer.data, 
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(serializer.errors, 
    #                     status=status.HTTP_400_BAD_REQUEST)

