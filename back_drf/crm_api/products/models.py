from django.db import models


class Country(models.Model):
    name = models.CharField(null=False, max_length=55)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(null=False, max_length=55)

    def __str__(self):
        return self.name


class Beverage(models.Model):
    name = models.CharField(null=False, max_length=55)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(null=False, max_length=55)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StockProduct(models.Model):
    stock_1 = models.IntegerField()
    stock_2 = models.IntegerField(null=True)
    stock_3 = models.IntegerField(null=True)
    product_year = models.CharField(max_length=15, null=True)
    date_of_arrival = models.DateField(null=True)


class CodeProduct(models.Model):
    code_1 = models.CharField(max_length=255)
    code_2 = models.CharField(max_length=255, null=True)
    code_3 = models.CharField(max_length=255, null=True)


class PriceProduct(models.Model):
    whole_sale_price = models.FloatField()
    retail_sale_price = models.FloatField()
    sale_price_3to5 = models.FloatField()
    sale_price_5to10 = models.FloatField()
    sale_price_above10 = models.FloatField()
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=False)


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    image = models.ImageField()
    alcohol_strength = models.FloatField()
    case_bottles_number = models.IntegerField(default=12)  # 6, 12, 24
    country = models.ManyToManyField(Country)
    region = models.ManyToManyField(Region)
    beverage = models.ManyToManyField(Beverage)
    state = models.ManyToManyField(State)
    code = models.OneToOneField(CodeProduct, on_delete=models.CASCADE)
    price = models.OneToOneField(PriceProduct, on_delete=models.CASCADE)
    stock = models.OneToOneField(StockProduct, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
