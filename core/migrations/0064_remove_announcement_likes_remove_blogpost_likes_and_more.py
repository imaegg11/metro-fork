# Generated by Django 4.0.10 on 2023-03-20 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_commenthistory_comment_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
