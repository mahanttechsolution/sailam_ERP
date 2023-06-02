# Generated by Django 4.0 on 2023-06-01 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_client_remove_memo_address_remove_memo_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memo',
            name='stk_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory', to_field='STK_ID'),
        ),
    ]