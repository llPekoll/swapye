# Generated by Django 4.0 on 2022-10-07 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authie", "0002_note"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="details",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="note",
            name="content",
            field=models.CharField(max_length=255),
        ),
    ]
