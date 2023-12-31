# Generated by Django 4.1.3 on 2023-02-04 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0040_alter_requestedelement_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ValidatedEmail",
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
                ("bouncer_return", models.JSONField()),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="validated_email",
                        to="games.game",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="lead",
            name="validated_email",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="games.validatedemail",
            ),
        ),
    ]
