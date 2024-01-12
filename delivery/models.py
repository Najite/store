from django.db import models
from uuid import uuid4
# Create your models here.
class Delivery(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    first_name = models.CharField(max_lenght=50)
    last_name = models.CharField(max_lenght=50)
    address = models.CharField(max_length=200)
    phone_number = models.PositiveIntegerField()
    


