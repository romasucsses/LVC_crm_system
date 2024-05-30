from rest_framework import serializers
from .models import *
from customers.serializers import CustomerSerializerAPI
from customers.models import *


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializerAPI()
    # customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Invoices
        fields = '__all__'
