from rest_framework import serializers
from .models import Product


class ProductsWithoutPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['case_bottles_number', 'price']


class ProductsWithPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
