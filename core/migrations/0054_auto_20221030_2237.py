# Generated by Django 3.2.12 on 2022-10-30 22:37

from django.db import migrations, models

import core.utils.fields


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0053_qltrs"),
    ]

    operations = [
        migrations.CreateModel(
            name="Raffle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("description", models.TextField(blank=True)),
                ("open_start", models.DateTimeField()),
                ("open_end", models.DateTimeField()),
                ("page_win", models.CharField(max_length=128)),
                ("page_lose", models.CharField(max_length=128)),
                (
                    "codes_win",
                    core.utils.fields.SetField(
                        blank=True, null=True, verbose_name="Winning Codes"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="announcement",
            name="show_after",
            field=models.DateTimeField(
                help_text="Show this announcement after this time.",
                verbose_name="Automatically post on",
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="show_after",
            field=models.DateTimeField(
                help_text="Show this announcement after this time.",
                verbose_name="Automatically post on",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="is_instructional",
            field=models.BooleanField(
                default=True,
                help_text="Whether school instruction is taking place during this event. Leave checked if not direct cause.",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="qltrs",
            field=core.utils.fields.SetField(
                blank=True, null=True, verbose_name="Qualified Trials"
            ),
        ),
    ]
