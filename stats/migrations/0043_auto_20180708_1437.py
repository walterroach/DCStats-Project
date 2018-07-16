# Generated by Django 2.0.2 on 2018-07-08 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0042_auto_20180707_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='all_aircraft_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='building_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='crash',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='death',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='eject',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='fighter_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='friendly_col_hits',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='friendly_col_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='friendly_hits',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='friendly_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='ground_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='heli_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mission',
            name='ship_kills',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
