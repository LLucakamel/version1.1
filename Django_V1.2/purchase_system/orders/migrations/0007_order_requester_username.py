# Generated by Django 5.0.7 on 2024-08-15 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='requester_username',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]
