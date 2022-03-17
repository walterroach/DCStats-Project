# Generated by Django 2.0.2 on 2018-07-17 02:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0059_auto_20180716_2157"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("in_air_sec", models.FloatField(null=True)),
                ("total_sec", models.FloatField(null=True)),
                ("crash", models.IntegerField(null=True)),
                ("eject", models.IntegerField(null=True)),
                ("death", models.IntegerField(null=True)),
                ("friendly_col_hits", models.IntegerField(null=True)),
                ("friendly_col_kills", models.IntegerField(null=True)),
                ("friendly_hits", models.IntegerField(null=True)),
                ("friendly_kills", models.IntegerField(null=True)),
                ("building_kills", models.IntegerField(null=True)),
                ("ground_kills", models.IntegerField(null=True)),
                ("heli_kills", models.IntegerField(null=True)),
                ("fighter_kills", models.IntegerField(null=True)),
                ("all_aircraft_kills", models.IntegerField(null=True)),
                ("ship_kills", models.IntegerField(null=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stats.Aircraft"
                    ),
                ),
                (
                    "mission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stats.Mission"
                    ),
                ),
                (
                    "pilot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stats.Pilot"
                    ),
                ),
            ],
        ),
    ]
