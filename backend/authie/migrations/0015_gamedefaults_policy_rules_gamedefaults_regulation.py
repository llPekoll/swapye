# Generated by Django 4.1.3 on 2023-02-24 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0014_gamedefaults_logo_gamedefaults_music"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamedefaults",
            name="policy_rules",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="gamedefaults",
            name="regulation",
            field=models.TextField(default=""),
        ),
    ]
