# Generated by Django 3.2.16 on 2022-11-13 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0005_useraccount_uuid"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInfo",
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
                    "mail_provider",
                    models.CharField(
                        choices=[("MailJet", "Mailjet"), ("Courier", "Courier")],
                        default="MailJet",
                        max_length=128,
                    ),
                ),
                (
                    "mail_apikey",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "mail_apipass",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("nom", models.CharField(blank=True, max_length=255, null=True)),
                ("first", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("cp", models.IntegerField(blank=True, null=True)),
                ("ville", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_infos",
                        to="authie.useraccount",
                    ),
                ),
            ],
        ),
    ]
