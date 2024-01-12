from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from orders.models import Order
# Create your models here.

User = get_user_model()

class Payment(models.Model):
    order_item = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_payment',
        null=True
    )
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4
    ) 
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                             related_name='user_payment')
    amount = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add =True)
    reference = models.UUIDField(
        primary_key=False,
        editable=False,
        default=uuid4
    )
    
    def __str__(self):
        return f"{self.user.username} made {self.amount} "
    


