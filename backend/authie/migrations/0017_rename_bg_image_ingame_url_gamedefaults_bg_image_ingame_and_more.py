# Generated by Django 4.1.3 on 2023-03-18 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0016_gamedefaults_bg_image_ingame_url_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gamedefaults",
            old_name="bg_image_ingame_url",
            new_name="bg_image_ingame",
        ),
        migrations.RenameField(
            model_name="gamedefaults",
            old_name="intro_image_url_landscape",
            new_name="form_landscape",
        ),
        migrations.RenameField(
            model_name="gamedefaults",
            old_name="intro_image_url_portrait",
            new_name="form_portrait",
        ),
    ]