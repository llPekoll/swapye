# Generated by Django 3.2.16 on 2022-11-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dash", "0003_alter_gametype_limite_users_alter_skin_limite_users"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="skin",
            constraint=models.UniqueConstraint(
                fields=("game", "name"), name="game_and_name"
            ),
        ),
    ]
