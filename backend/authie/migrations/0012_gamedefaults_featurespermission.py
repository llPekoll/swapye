# Generated by Django 4.1.3 on 2023-02-03 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0011_auto_20221125_1734"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameDefaults",
            fields=[
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="authie.useraccount",
                    ),
                ),
                ("email_check", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="FeaturesPermission",
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
                ("name", models.CharField(max_length=255)),
                ("trial", models.BooleanField(default=False)),
                ("basic", models.BooleanField(default=False)),
                ("plus", models.BooleanField(default=False)),
                ("premium", models.BooleanField(default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to="authie.useraccount",
                    ),
                ),
            ],
        ),
    ]
