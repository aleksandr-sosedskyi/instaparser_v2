# Generated by Django 3.1 on 2020-08-27 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_controller_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='instauser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]