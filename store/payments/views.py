from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all() 
    serializer_class = PaymentSerializer

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success_message = 'Payment succesfull'
        headers = self.get_success_headers(serializer.data)
        
        return Response (
            {
                "message": success_message,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )