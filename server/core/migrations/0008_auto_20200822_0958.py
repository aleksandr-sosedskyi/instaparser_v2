# Generated by Django 3.1 on 2020-08-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200822_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='instauser',
            name='subscribers',
            field=models.PositiveIntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='process',
            name='tid',
            field=models.PositiveIntegerField(default=123),
            preserve_default=False,
        ),
    ]
