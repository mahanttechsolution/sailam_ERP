# Generated by Django 4.0 on 2023-05-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_role_role_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_status',
            field=models.CharField(choices=[(2, 'passive'), (1, 'active')], default=1, max_length=20),
        ),
    ]
