from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from products.models import Product


User = get_user_model()

# Create your models here.
# creating the order
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='order'
    )
    order_status_choice = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered")
    ]
    order_status = models.CharField(max_length=15, 
                                    choices=order_status_choice,
                                    default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.00
    )

    def save(self, *args, **kwargs):
        self.update_total_price()
        super().save(*args, **kwargs)
    
    def update_total_price(self):
        self.total_price = sum(item.total_price for item in self.order_item.all())


# creating the order item
class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_item'
    )
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE,
                                related_name='product')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0.00
                                      )
    
    def save(self, *args, **kwargs):
        self.update_total_price()
        super().save(*args, **kwargs)
    
    def update_toal_price(self):
        self.total_price = self.quantity * self.product.price
    