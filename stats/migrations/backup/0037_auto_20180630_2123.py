# Generated by Django 2.0.2 on 2018-07-01 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0036_auto_20180630_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='aircraft',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.Aircraft'),
        ),
    ]
