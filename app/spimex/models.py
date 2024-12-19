
from django.db import models
from datetime import datetime


class SpimexTradingResults(models.Model):
    exchange_product_id = models.CharField(max_length=255)
    exchange_product_name = models.CharField(max_length=255)
    oil_id = models.CharField(max_length=255)
    delivery_basis_id = models.CharField(max_length=255)
    delivery_basis_name = models.CharField(max_length=255)
    delivery_type_id = models.CharField(max_length=255)
    volume = models.IntegerField()
    total = models.IntegerField()
    count = models.IntegerField()
    date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.now()
        self.updated_on = datetime.now()
        super().save(*args, **kwargs)
