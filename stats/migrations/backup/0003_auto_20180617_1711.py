# Generated by Django 2.0.2 on 2018-06-17 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0002_auto_20180617_1709"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="Pilot",
        ),
    ]
