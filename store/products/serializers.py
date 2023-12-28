from rest_framework import serializers
from .models import Product



class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Product
        fields = ['id',
                  'user',
                  'name',
                  'price',
                  'image',
                  'created_at',
                  'updated_at',
                  'category'
                  
                  ]



