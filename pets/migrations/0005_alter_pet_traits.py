# Generated by Django 4.2.4 on 2023-08-21 00:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0003_rename_created_ate_trait_created_at"),
        ("pets", "0004_alter_pet_traits"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="traits",
            field=models.ManyToManyField(related_name="pets", to="traits.trait"),
        ),
    ]
