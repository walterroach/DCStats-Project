# Generated by Django 2.0.2 on 2018-07-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0038_auto_20180630_2148"),
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
                    ("Guest", "Guest"),
                ],
                max_length=3,
            ),
        ),
    ]
