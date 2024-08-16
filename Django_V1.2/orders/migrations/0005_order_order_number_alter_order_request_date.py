# Generated by Django 5.0.7 on 2024-08-13 08:24

from django.db import migrations, models
import random

def generate_order_numbers(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    orders = Order.objects.all()
    for order in orders:
        order.order_number = random.randint(10000, 99999)  # or any other logic to generate unique numbers
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_due_date_order_request_date_order_supply_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(generate_order_numbers),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='request_date',
            field=models.DateField(),
        ),
    ]