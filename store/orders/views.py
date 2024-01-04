from rest_framework.viewsets import ReadOnlyModelViewSet
from .serialzers import OrderItemSerializer, OrderSerializer
from .models import Order, OrderItem

class OrderViewset(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
