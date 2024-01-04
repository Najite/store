from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                             related_name='user_payment')
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} made {self.amount} "
    
    

