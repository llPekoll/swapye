# Generated by Django 4.0 on 2022-10-07 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0003_useraccount_details_alter_note_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="details",
            field=models.TextField(blank=True, null=True),
        ),
    ]