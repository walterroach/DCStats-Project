# Generated by Django 2.0.2 on 2018-06-26 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0024_auto_20180619_1135"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Slmod_Total",
        ),
        migrations.RemoveField(
            model_name="total",
            name="aircraft",
        ),
        migrations.RemoveField(
            model_name="total",
            name="pilot",
        ),
        migrations.DeleteModel(
            name="Total",
        ),
    ]
