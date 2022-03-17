# Generated by Django 2.0.2 on 2018-06-18 00:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0011_auto_20180617_1923"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rank",
            old_name="pilot",
            new_name="pilot_id",
        ),
        migrations.AddField(
            model_name="pilot",
            name="rank_id",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="stats.Rank"
            ),
            preserve_default=False,
        ),
    ]
