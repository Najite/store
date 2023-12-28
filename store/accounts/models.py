from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.utils.translation import gettext_lazy as _
import uuid

# Creating the custom user models
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,password):
        user = self.create_user(
            email,
            password=password
        )
        user.staff=True
        user.admin=True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser):
    id =  models.UUIDField(primary_key=True,
                           editable=False,
                           default=uuid.uuid4)
    firstname = models.CharField(_("firstname"), max_length=150)
    lastname = models.CharField(_("Lastname"), max_length=150)
    username = models.CharField(_("Username"), max_length=60)
    email = models.EmailField(
        verbose_name = "email address",
        max_length = 100,
        unique = True
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # admin user but not superuser
    admin = models.BooleanField(default=False) # the superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email
    
    def get_email(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin



    
