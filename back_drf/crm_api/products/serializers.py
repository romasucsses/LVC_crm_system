from rest_framework import serializers
from .models import *


class ProductsWithoutPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['price']


class ProductsWithPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = '__all__'


class CodeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeProduct
        fields = '__all__'


class PriceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceProduct
        fields = '__all__'
