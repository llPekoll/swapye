# Generated by Django 3.2.16 on 2022-11-29 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0024_auto_20221129_1245"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="font",
        ),
    ]
