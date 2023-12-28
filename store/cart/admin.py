from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'cart_status',
        'creation_date',
        'modification_date',
        'total_price',
    ]
    search_fields = ['user']
    list_filter = ['cart_status']

@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = [
        'id',
        'cart',
        'product',
        'quantity',
        'total_price'
    ]

