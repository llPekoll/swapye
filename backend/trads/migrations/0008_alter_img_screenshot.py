# Generated by Django 4.0 on 2022-03-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trads", "0007_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="img",
            name="screenshot",
            field=models.FileField(upload_to="web/img"),
        ),
    ]
