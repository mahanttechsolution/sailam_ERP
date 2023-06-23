# Generated by Django 4.0 on 2023-06-21 01:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_inventory_tallymade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tallydata',
            old_name='Submitted',
            new_name='submitted',
        ),
        migrations.AddField(
            model_name='tallydata',
            name='tally_no',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.tally'),
            preserve_default=False,
        ),
    ]