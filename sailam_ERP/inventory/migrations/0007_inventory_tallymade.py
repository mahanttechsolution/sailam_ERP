# Generated by Django 4.0 on 2023-06-20 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_tallydata_tally'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='TallyMade',
            field=models.BooleanField(default=False),
        ),
    ]
