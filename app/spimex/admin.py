from django.contrib import admin
from .models import SpimexTradingResults


@admin.register(SpimexTradingResults)
class SpimexTradingResultsAdmin(admin.ModelAdmin):
    list_display = (
        'exchange_product_id', 'exchange_product_name', 'oil_id',
        'delivery_basis_id', 'delivery_basis_name', 'delivery_type_id',
        'volume', 'total', 'count', 'date', 'created_on', 'updated_on'
    )

    search_fields = (
        'exchange_product_id', 'exchange_product_name', 'oil_id',
        'delivery_basis_id', 'delivery_basis_name', 'delivery_type_id',
        'volume', 'total', 'count', 'date'
    )

    list_filter = (
        'exchange_product_id', 'oil_id', 'delivery_basis_id',
        'delivery_type_id', 'date', 'created_on', 'updated_on'
    )

    list_editable = ('volume', 'total', 'count')

    ordering = ('-date', 'exchange_product_id')
