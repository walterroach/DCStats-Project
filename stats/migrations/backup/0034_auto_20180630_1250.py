# Generated by Django 2.0.2 on 2018-06-30 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0033_auto_20180629_2158"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aircraft",
            name="date",
        ),
        migrations.RemoveField(
            model_name="aircraft",
            name="in_air_sec",
        ),
        migrations.RemoveField(
            model_name="aircraft",
            name="total_sec",
        ),
        migrations.AlterField(
            model_name="mission",
            name="aircraft",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="stats.Aircraft"
            ),
        ),
        migrations.AlterField(
            model_name="mission",
            name="date",
            field=models.DateTimeField(),
        ),
    ]
