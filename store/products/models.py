from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# creating the Category for the model
class Category(models.Model):
    name = models.CharField(_("name"), max_length=100,
                            help_text=_("Name of the category"))
    
    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx"),
        ]
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


# Creating the products model
class Product(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False) 
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=100,
                            help_text=_("Name of the product"))
    price = models.DecimalField(_("price"), max_digits=7, 
                                decimal_places=2, default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE,
                                 related_name="category") 
    
    image = models.ImageField(upload_to="product/")


    
    class Meta:
        indexes = [
            models.Index(fields=["name", "price", 
                                 "category"
                                 ]
                        )
        ]
    
    def __str__(self):
        return self.name