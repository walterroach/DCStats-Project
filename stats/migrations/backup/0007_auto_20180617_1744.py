# Generated by Django 2.0.2 on 2018-06-17 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0006_auto_20180617_1738"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rank",
            name="rank",
            field=models.CharField(
                choices=[
                    ("O1", "O-1"),
                    ("O2", "O-2"),
                    ("O3", "O-3"),
                    ("O4", "O-4"),
                    ("O5", "O-5"),
                    ("O6", "O-6"),
                ],
                max_length=3,
            ),
        ),
    ]
