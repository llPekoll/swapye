# Generated by Django 4.1.3 on 2023-03-19 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "authie",
            "0017_rename_bg_image_ingame_url_gamedefaults_bg_image_ingame_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gamedefaults",
            name="bg_image_ingame",
        ),
        migrations.RemoveField(
            model_name="gamedefaults",
            name="form_landscape",
        ),
        migrations.RemoveField(
            model_name="gamedefaults",
            name="form_portrait",
        ),
    ]
