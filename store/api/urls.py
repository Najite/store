from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import (
    ProductViewList, CategoryViewList
)
from cart.views import CartView
router = DefaultRouter()

router.register('product', ProductViewList, basename='product')
router.register('category', CategoryViewList, basename='category')
router.register('cart', CartView, basename='cart')
urlpatterns = router.urls
 