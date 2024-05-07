from django.db import models
from products.models import State


class Customer(models.Model):
    name = models.CharField(max_length=355, null=False)
    address = models.CharField(max_length=455, null=False)
    google_maps_path = models.TextField()
    phone = models.CharField(max_length=155)
    contact_person = models.CharField(max_length=55)
    zip_code = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=355)
    open_at_hour = models.TimeField()
    licence_number = models.CharField(max_length=355)
    price_type = models.CharField(max_length=55)
    last_call = models.DateField(null=True)
    last_visiting = models.DateField(null=True)
    last_testing = models.DateField(null=True)
    last_order = models.DateField(null=True)
    state = models.ManyToManyField(State)
    email = models.EmailField()

    def __str__(self):
        return self.name
