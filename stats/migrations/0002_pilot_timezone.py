# Generated by Django 2.0.2 on 2018-07-22 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='timezone',
            field=models.CharField(default='UTC', max_length=30),
        ),
    ]
