# Generated by Django 4.2.11 on 2024-04-18 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_routing'),
    ]

    operations = [
        migrations.AddField(
            model_name='routing',
            name='routing',
            field=models.CharField(default='', editable=False, max_length=255, unique=True),
        ),
    ]
