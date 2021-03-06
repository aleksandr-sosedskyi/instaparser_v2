# Generated by Django 3.1 on 2020-09-03 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_auto_20200902_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='queue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.queue'),
        ),
        migrations.AlterField(
            model_name='instauser',
            name='group',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=3),
        ),
        migrations.AlterField(
            model_name='process',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.instauser'),
        ),
    ]
