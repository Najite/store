from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import (
    Product, Category
)
from .serializers import (
    ProductListSerializer,
    CategoryListSerializer,
    CategoryDetaiSerializer
)

class ProductViewList(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# category views
class CategoryViewList(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


    def get_serializer_class(self):
        if (self.action == 'retrieve'):
            return CategoryDetaiSerializer
        return super().get_serializer_class()

        
