# Generated by Django 4.2.13 on 2024-08-05 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_appuser_bio_alter_appuser_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="name",
            field=models.CharField(
                help_text="this will be visible to others", max_length=50
            ),
        ),
    ]
