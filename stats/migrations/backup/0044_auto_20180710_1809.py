# Generated by Django 2.0.2 on 2018-07-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0043_auto_20180708_1437"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="date",
            field=models.DateField(),
        ),
    ]
