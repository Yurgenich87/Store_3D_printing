from rest_framework import serializers
from .models import Product, User, Order, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Form for creating new Orders"""
    class Meta:
        model = Order
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """Form for creating new Category"""
    class Meta:
        model = Category
        fields = '__all__'
