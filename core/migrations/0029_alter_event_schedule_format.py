# Generated by Django 3.2.6 on 2021-09-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210901_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='schedule_format',
            field=models.CharField(default='default', max_length=64),
        ),
    ]
