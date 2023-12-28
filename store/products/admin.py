from django.contrib import admin
from products.models import Product, Category
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = [
        "name", "price",
        "category",
        "created_at",
        "updated_at",
        
    ]
    list_filter = [
        "created_at",
        "updated_at",
        "price"
    ]

    def save_model(self, request, obj, form, change):
        # associate the current user to product
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(pk=request.user.id)
            kwargs["initial"] = request.user.id 
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdminList(admin.ModelAdmin):
    list_display = [
        "name"
    ]