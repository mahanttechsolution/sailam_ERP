# Generated by Django 4.0 on 2023-06-15 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_role_role_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_status',
            field=models.CharField(choices=[(2, 'passive'), (1, 'active')], default=1, max_length=20),
        ),
    ]
