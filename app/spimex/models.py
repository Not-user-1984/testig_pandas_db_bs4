
from django.db import models


class SpimexTradingResults(models.Model):
    id = models.AutoField(primary_key=True)
    exchange_product_id = models.CharField(max_length=100)
    exchange_product_name = models.CharField(max_length=255)
    oil_id = models.CharField(max_length=100)
    delivery_basis_id = models.CharField(max_length=100)
    delivery_basis_name = models.CharField(max_length=255)
    delivery_type_id = models.CharField(max_length=100)
    volume = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    date = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    def __str__(self):
        return f"{self.exchange_product_name} - {self.date}"
