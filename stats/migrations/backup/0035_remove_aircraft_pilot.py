# Generated by Django 2.0.2 on 2018-06-30 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0034_auto_20180630_1250"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aircraft",
            name="pilot",
        ),
    ]
