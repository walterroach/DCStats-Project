# Generated by Django 2.0.2 on 2018-07-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0063_remove_stats_new"),
    ]

    operations = [
        migrations.AddField(
            model_name="stats",
            name="new",
            field=models.IntegerField(default=0),
        ),
    ]
