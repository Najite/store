from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    readonly_fields = ['id']
    model = OrderItem
    fields = [
        'id',
        'order',
        'product',
        'quantity',
        'total_price',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]