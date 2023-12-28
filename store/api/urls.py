from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import (
    ProductViewList, CategoryViewList
)

router = DefaultRouter()

router.register('product', ProductViewList, basename='product')
router.register('category', CategoryViewList, basename='category')
urlpatterns = router.urls
