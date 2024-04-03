# Generated by Django 4.2.5 on 2024-04-03 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_remove_module_faculty_module_semester_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="code",
            field=models.CharField(default="ACME", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="module",
            name="name",
            field=models.CharField(default="NAME", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="module",
            name="password",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="university",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.university",
            ),
        ),
    ]