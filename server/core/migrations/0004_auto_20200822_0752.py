# Generated by Django 3.1 on 2020-08-22 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200822_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instauser',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]
