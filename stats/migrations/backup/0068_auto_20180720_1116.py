# Generated by Django 2.0.2 on 2018-07-20 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0067_auto_20180719_1319"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pilot",
            name="f_name",
        ),
        migrations.RemoveField(
            model_name="pilot",
            name="l_name",
        ),
    ]
