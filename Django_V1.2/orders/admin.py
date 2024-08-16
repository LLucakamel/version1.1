from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number',)
    list_display = ('order_number', 'product_name', 'quantity', 'supply_date', 'request_date')