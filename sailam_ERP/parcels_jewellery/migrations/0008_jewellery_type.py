# Generated by Django 4.0 on 2023-06-13 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parcels_jewellery', '0007_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewellery',
            name='Type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='parcels_jewellery.type'),
            preserve_default=False,
        ),
    ]