# Generated by Django 2.0.2 on 2018-07-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0066_auto_20180718_1839"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stats",
            name="aar",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="aircraft_kills",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="ground_kills",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="in_air_sec",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="landings",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="losses",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="ship_kills",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="total_sec",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="traps",
            field=models.IntegerField(default=0),
        ),
    ]
