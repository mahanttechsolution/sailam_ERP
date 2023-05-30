# Generated by Django 4.0 on 2023-05-30 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_inventory_scan_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='PURITY',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='SIZE',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='STK_NO',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='CLARITY',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='COLOR',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='CUT',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='DEPTH',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='DESCRIPTION',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='FLO_COL',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='GIA_NO',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='MESUREMNT',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='POL',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='REMARK',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='SHAPE',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='SYM',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='TABLE',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
