from rest_framework import serializers
from categories.models import *
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['id', 'image', 'category', 'is_active'] 

class CategoryDetailSerializer(serializers.ModelSerializer):
    prdocuts = ProductSerializer(many = True, read_only = True)
    images = CategoryImageSerializer(many = True, read_only = True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'images']