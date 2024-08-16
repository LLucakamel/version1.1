from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='due_date',
            new_name='supply_date',
        ),
        migrations.AddField(
            model_name='order',
            name='request_date',
            field=models.DateField(default=datetime.date.today().isoformat()),  # Ensure this is a string
        ),
    ]