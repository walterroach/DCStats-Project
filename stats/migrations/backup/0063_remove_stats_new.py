# Generated by Django 2.0.2 on 2018-07-17 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0062_stats_new"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stats",
            name="new",
        ),
    ]
