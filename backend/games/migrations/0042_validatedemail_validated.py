# Generated by Django 4.1.3 on 2023-02-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0041_validatedemail_lead_validated_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="validatedemail",
            name="validated",
            field=models.BooleanField(default=False),
        ),
    ]
