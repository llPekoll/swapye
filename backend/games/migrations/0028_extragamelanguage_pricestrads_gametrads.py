# Generated by Django 4.1.3 on 2022-12-10 20:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0027_remove_game_end_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtraGameLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lang",
                    models.CharField(
                        max_length=2,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                ("id_ref", models.IntegerField(default=1)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="extra_langagues",
                        to="games.game",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PricesTrads",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("img", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "extra_game_language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price_traductions",
                        to="games.extragamelanguage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameTrads",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "opening_text",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "closing_text",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "extra_game_language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_traductions",
                        to="games.extragamelanguage",
                    ),
                ),
            ],
        ),
    ]
