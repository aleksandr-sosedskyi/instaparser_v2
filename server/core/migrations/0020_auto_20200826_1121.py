# Generated by Django 3.1 on 2020-08-26 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_controller_is_stopped'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controller',
            options={'verbose_name': 'Controller', 'verbose_name_plural': 'Controllers'},
        ),
    ]
