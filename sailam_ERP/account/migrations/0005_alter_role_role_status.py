# Generated by Django 4.0 on 2023-06-16 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_role_role_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_status',
            field=models.CharField(choices=[(1, 'active'), (2, 'passive')], default=1, max_length=20),
        ),
    ]
