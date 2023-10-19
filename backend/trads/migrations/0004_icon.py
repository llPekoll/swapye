# Generated by Django 4.0 on 2022-02-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trads", "0003_rename_key_img_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="Icon",
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
                ("key", models.CharField(max_length=32, unique=True)),
                ("link", models.TextField(default="")),
            ],
        ),
    ]
