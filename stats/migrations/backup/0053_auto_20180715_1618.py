# Generated by Django 2.0.2 on 2018-07-15 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0052_auto_20180715_1519"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="file",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="mission",
            name="name",
            field=models.CharField(max_length=250, null=True),
        ),
    ]
