# Generated by Django 4.0 on 2022-10-09 19:24

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0004_alter_useraccount_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]