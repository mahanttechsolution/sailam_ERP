# Generated by Django 4.0 on 2023-05-24 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_role_role_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_status',
            field=models.CharField(choices=[(1, 'active'), (2, 'passive')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='account.role'),
        ),
    ]
