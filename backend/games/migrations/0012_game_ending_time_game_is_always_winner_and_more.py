# Generated by Django 4.0 on 2022-10-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0011_lead_price_won"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="ending_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="game",
            name="is_always_winner",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="game",
            name="starting_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="game",
            name="timezone",
            field=models.CharField(
                choices=[("Europe/Paris", "Eu")], default="Europe/Paris", max_length=128
            ),
        ),
        migrations.AddField(
            model_name="price",
            name="display_price_name",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="price",
            name="offset_price_name",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]