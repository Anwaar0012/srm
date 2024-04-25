# Generated by Django 4.2.11 on 2024-04-18 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0014_remove_invoice_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
