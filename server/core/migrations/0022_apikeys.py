# Generated by Django 3.1 on 2020-08-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200826_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
            ],
        ),
    ]