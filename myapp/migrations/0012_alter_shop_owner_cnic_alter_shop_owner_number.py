<<<<<<< HEAD
# Generated by Django 4.2.11 on 2024-04-18 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_routing_routing_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='owner_cnic',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
=======
# Generated by Django 4.2.11 on 2024-04-18 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_routing_routing_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='owner_cnic',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
>>>>>>> origin/main
