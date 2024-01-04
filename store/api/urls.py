from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from products.views import (
    ProductViewList, CategoryViewList
)
from cart.views import CartView, CartItemView

router = DefaultRouter()

router.register('product', ProductViewList, basename='product')
router.register('category', CategoryViewList, basename='category')
router.register('cart', CartView, basename='cart')

cart_router = routers.NestedDefaultRouter(
    router, 'cart', lookup='cart'
)

cart_router.register('items', CartItemView, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls))
]