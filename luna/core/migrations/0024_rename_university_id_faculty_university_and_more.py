# Generated by Django 4.2.5 on 2024-03-25 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_module_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="faculty",
            old_name="university_id",
            new_name="university",
        ),
        migrations.AddField(
            model_name="user",
            name="university",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.university",
            ),
        ),
    ]
