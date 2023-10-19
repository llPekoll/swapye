# Generated by Django 4.0 on 2022-08-13 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authie", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                ("emblem", models.CharField(default="Jose", max_length=32)),
                ("game_name", models.CharField(max_length=128)),
                (
                    "game_type",
                    models.CharField(
                        choices=[("curtain", "Curtain")],
                        default="curtain",
                        max_length=128,
                    ),
                ),
                (
                    "game_theme",
                    models.CharField(
                        choices=[("base", "Base")], default="base", max_length=128
                    ),
                ),
                ("request_name", models.BooleanField(default=True)),
                ("request_email", models.BooleanField(default=True)),
                ("request_tel", models.BooleanField(default=True)),
                ("request_address", models.BooleanField(default=True)),
                ("request_cp", models.BooleanField(default=True)),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("unlimited_in_time", models.BooleanField(default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games",
                        to="authie.useraccount",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WinnedPrice",
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
                    "price",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="winned_prices",
                        to="games.game",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Price",
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
                ("name", models.CharField(max_length=32)),
                ("img", models.FileField(upload_to="games/img")),
                ("number", models.IntegerField(default=10)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="games.game",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lead",
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
                ("email", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("tel", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("cp", models.CharField(blank=True, max_length=255, null=True)),
                ("can_reveceive_email", models.BooleanField(default=True)),
                ("creation_date", models.DateTimeField(auto_now=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leads",
                        to="games.game",
                    ),
                ),
            ],
        ),
    ]