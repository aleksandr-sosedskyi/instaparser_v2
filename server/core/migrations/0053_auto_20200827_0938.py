# Generated by Django 3.1 on 2020-08-27 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_speedlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='speedlog',
            options={'ordering': ('-created_at',), 'verbose_name': 'Speed Log', 'verbose_name_plural': 'Speed Logs'},
        ),
        migrations.RemoveField(
            model_name='speedlog',
            name='date',
        ),
        migrations.AddField(
            model_name='speedlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
