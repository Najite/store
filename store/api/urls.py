from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import ProductViewList

router = DefaultRouter()

router.register('product', ProductViewList)
urlpatterns = router.urls
