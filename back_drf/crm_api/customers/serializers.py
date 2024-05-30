from rest_framework import serializers
from .models import Customer


class CustomerSerializerAPI(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "name",
            "address",
           "google_maps_path",
           "phone",
           "contact_person",
           "zip_code",
           "tax_id",
           "open_at_hour",
           "licence_number",
           "price_type",
           "last_call",
           "last_visiting",
           "last_testing",
           "last_order",
           "state",
           "email"
        ]
