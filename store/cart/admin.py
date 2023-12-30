from django.contrib import admin
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()

# @admin.register(CartItem)
class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['id']
    # model = CartItem
    fields = [
        "id",
        'cart',
        'product',
        'quantity',
        'total_price',
    ]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = [
        'id',
        'user',
        'cart_status',
        'total_price'
    ]
    inlines = [
        CartItemInline
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.pk:
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)
        
        open_orders = Order.objects.filter(
            user=obj.user,
            order_status="Pending")
        
        if open_orders.exists():
            order = open_orders.first()
        else:
            order = Order.objects.create(user=obj.user)

        for cart_item in obj.cartitem_set.all():
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=cart_item.product
            )
            order_item.quantity = cart_item.quantity
            order_item.total_price = cart_item.total_price
            order_item.save()
        
        order.save()

    def save_formset(self, request, form, formset, change):
        if form.instance.pk and formset.model == CartItem:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.cart = form.instance
                instance.save()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(
                pk=request.user.id
            )
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)