# Generated by Django 4.0 on 2022-10-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0014_refusedlead_alter_game_timezone"),
    ]

    operations = [
        migrations.AddField(
            model_name="refusedlead",
            name="creation_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
