# Generated by Django 4.0 on 2023-06-17 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_inventory_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='Match',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
