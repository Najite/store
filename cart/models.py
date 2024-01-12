from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from products.models import Product
from uuid import uuid4


User = get_user_model()

# creating the logic for cart
class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        # editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='cart_user'
    )
    cart_status_choice = [
        ('Open', 'Open'),
        ('Checked out', 'Checked out'),
    ]
    cart_status = models.CharField(max_length=120,
                                   choices=cart_status_choice,
                                   default="Open")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, 
                                      decimal_places=2,
                                      default=0.00
                                      )
    

    def update_total_price(self):
        print('got called')
        total_price = self.cartitems.aggregate(Sum(
            'total_price'
            ))['total_price__sum'] or 0
        self.total_price = total_price
        self.save()
            

# creating the cart item
class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    cart = models.ForeignKey(
        Cart,on_delete=models.CASCADE,
        related_name='cartitems'
    )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                # related_name='item'
                                )
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, 
                                      decimal_places=2, default=0.00
                                      )
    
    def save(self, *args, **kwargs):
        self.update_total_price()
        return super().save(*args, **kwargs)

    def update_total_price(self):
        self.total_price = self.quantity * self.product.price
        

    

