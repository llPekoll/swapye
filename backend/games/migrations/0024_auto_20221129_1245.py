# Generated by Django 3.2.16 on 2022-11-29 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0023_auto_20221129_1241"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="color",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="game",
            name="font",
            field=models.CharField(
                choices=[("Roboto", "Roboto")], default="Roboto", max_length=128
            ),
        ),
    ]
