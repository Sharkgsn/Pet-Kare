# Generated by Django 4.2.4 on 2023-08-21 01:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0004_rename_name_trait_trait_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trait",
            old_name="trait_name",
            new_name="name",
        ),
    ]
