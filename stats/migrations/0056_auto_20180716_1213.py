# Generated by Django 2.0.2 on 2018-07-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0055_auto_20180716_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='date_time',
        ),
        migrations.AlterField(
            model_name='mission',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
