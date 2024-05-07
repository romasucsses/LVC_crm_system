from rest_framework import serializers
from .models import *


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        fields = '__all__'
