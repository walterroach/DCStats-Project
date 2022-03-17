# Generated by Django 2.0.2 on 2018-06-30 02:24

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0030_auto_20180629_2012"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aircraft",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2018, 6, 30, 2, 24, 3, 795599, tzinfo=utc)
            ),
        ),
        migrations.AlterField(
            model_name="mission",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2018, 6, 30, 2, 24, 3, 795599, tzinfo=utc)
            ),
        ),
    ]
