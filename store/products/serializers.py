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
        fields = ["name", 'id', 'url']

    def get_url(self, obj):
        request = self.context['request']
        return {
            'url': reverse('category-detail',
                           kwargs={'pk':obj.id},
                           request=request)
        }


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'name',
            'price',
            'image',
            'category',
            'category_id'
        ]
class CategoryDetaiSerializer(serializers.ModelSerializer):
    item = CategoryProductSerializer(many=True)
    class Meta:
        model = Category
        fields = [
            'name',
            'id',
            'item'
        ]


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
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
                  'category_id',
                  'url'          
                  ]


    def create(self, validated_data):
        category_id = validated_data.pop("category_id", None)
        if category_id:
            category = Category.objects.get(id=category_id)
            validated_data['category'] = category
        
        return super().create(validated_data)
    
    def validate_category_id(self, value):
        if not Category.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no category associated with that id")
        return value



