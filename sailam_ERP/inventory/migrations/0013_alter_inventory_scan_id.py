# Generated by Django 4.0 on 2023-05-29 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_alter_inventory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='Scan_Id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]