# Generated by Django 2.0.2 on 2018-06-18 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0010_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="total",
            name="pilot",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="stats.Pilot",
            ),
        ),
        migrations.AddField(
            model_name="total",
            name="total",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
