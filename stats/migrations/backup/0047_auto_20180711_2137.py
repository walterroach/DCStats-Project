# Generated by Django 2.0.2 on 2018-07-12 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0046_mission_ip_flag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="ip_flag",
            field=models.IntegerField(null=True),
        ),
    ]
