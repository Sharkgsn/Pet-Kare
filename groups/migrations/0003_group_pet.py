# Generated by Django 4.2.4 on 2023-08-20 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_remove_pet_group"),
        ("groups", "0002_alter_group_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="pet",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="group",
                to="pets.pet",
            ),
        ),
    ]
