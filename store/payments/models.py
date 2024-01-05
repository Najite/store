from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
# Create your models here.

User = get_user_model()

class Payment(models.Model):
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
    
    def __str__(self):
        return f"{self.user.username} made {self.amount} "
    


