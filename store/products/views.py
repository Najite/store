from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Product
from .serializers import ProductListSerializer

class ProductViewList(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductListSerializer
