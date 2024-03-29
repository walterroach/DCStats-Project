# Generated by Django 2.0.2 on 2018-07-07 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0041_auto_20180707_1835"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pilot",
            name="f_name",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="pilot",
            name="l_name",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="pilot",
            name="rank_id",
            field=models.ForeignKey(
                default=7,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="stats.Rank",
            ),
        ),
    ]
