# Generated by Django 4.2.11 on 2024-04-24 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0025_alter_invoice_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('updated_date', models.DateField(auto_now=True)),
                ('new_paid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customer_email',
            field=models.TextField(blank=True, null=True),
        ),
    ]
