# Generated by Django 3.1 on 2020-08-27 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20200826_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
