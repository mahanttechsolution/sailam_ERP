# Generated by Django 4.0 on 2023-05-29 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='id_inv',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory'),
            preserve_default=False,
        ),
    ]
