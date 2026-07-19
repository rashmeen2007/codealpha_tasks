from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.customer.name} - {self.product.name}"