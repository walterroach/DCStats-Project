# Generated by Django 2.0.2 on 2018-07-17 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0057_pilot_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stats",
            name="pilot",
        ),
    ]
