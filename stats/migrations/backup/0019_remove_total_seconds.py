# Generated by Django 2.0.2 on 2018-06-18 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0018_auto_20180618_1416"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="total",
            name="seconds",
        ),
    ]
