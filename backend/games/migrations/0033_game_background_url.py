# Generated by Django 4.1.3 on 2022-12-26 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0032_game_dry_run_game_force_result_cant_replay_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="background_url",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]