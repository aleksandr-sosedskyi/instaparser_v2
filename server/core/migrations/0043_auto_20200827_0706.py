# Generated by Django 3.1 on 2020-08-27 07:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200827_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='checked_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 7, 6, 1, 675065, tzinfo=utc)),
        ),
    ]