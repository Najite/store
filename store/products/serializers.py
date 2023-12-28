from rest_framework import serializers
from .models import (
    Product, Category,
    Review, Tag
)
from rest_framework.reverse import reverse

class CategoryListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["name", 'id', 'url', 'item']

    def get_url(self, obj):
        request = self.context['request']
        return {
            'url': reverse('category-detail',
                           kwargs={'pk':obj.id},
                           request=request)
        }

class CategoryDetaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'id',
            'product'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    category = CategoryListSerializer(read_only=True)
    category_id = serializers.UUIDField(
        write_only=True 
    )
    class Meta:
        model = Product
        fields = ['id',
                  'user',
                  'name',
                  'price',
                  'image',
                  'stock_quantity',
                  'is_available',
                  'tags',
                  'created_at',
                  'updated_at',
                  'category',
                  'category_id'             
                  ]


    def create(self, validated_data):
        category_id = validated_data.pop("category_id", None)
        if category_id:
            category = Category.objects.get(id=category_id)
            validated_data['category'] = category
        
        return super().create(validated_data)



