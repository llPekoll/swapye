# Generated by Django 4.0 on 2022-10-27 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0012_game_ending_time_game_is_always_winner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="losing_factor",
            field=models.IntegerField(default=50),
        ),
    ]
