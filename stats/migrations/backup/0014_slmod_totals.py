# Generated by Django 2.0.2 on 2018-06-18 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0013_remove_rank_pilot_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Slmod_Totals",
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
                ("file", models.FileField(upload_to="SlmodStats/%Y/%m/")),
            ],
        ),
    ]
