from django.db import models
from users.models import User
from customers.models import Customer


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer = models.ManyToManyField(Customer)
    cart_data = models.JSONField()
    cases_number = models.IntegerField()
    total_sum = models.FloatField()
    date_creating = models.DateField(auto_now=True)
    delivery_date = models.DateField()
    is_approved = models.BooleanField(default=False)


class Invoices(models.Model):
    code_invoice = models.CharField(max_length=355)
    code_order_invoice = models.CharField(max_length=355)
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    cart_data = models.JSONField()
    total_cases = models.IntegerField()
    total_sum = models.FloatField()
    past_due = models.CharField(max_length=55)
    is_sent_mail = models.BooleanField(default=False)
    ship_via = models.CharField(max_length=100, default='warehouse')  # warehouse/handle
    terms = models.CharField(max_length=55)








