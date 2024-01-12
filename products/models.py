from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# creating the Category for the model
class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(_("name"), max_length=100,
                            help_text=_("Name of the category"))
    
    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx"),
        ]
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

# creating tags
class Tag(models.Model):
    name = models.CharField(max_length=140,
                            unique=True
                            )
    
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
                                 related_name="item") 
    
    image = models.ImageField(upload_to="product/", blank=True,
                              null=True)
    stock_quantity = models.PositiveBigIntegerField()
    is_available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    
    def __str__(self):
        return self.name


    class Meta:
        indexes = [
            models.Index(fields=["name", "price", 
                                 "category"
                                 ]
                        )
        ]
    
    def __str__(self):
        return self.name
    

class Review(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_review")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} -{self.rating}"