# Generated by Django 4.2.5 on 2024-02-08 09:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_remove_module_resource_id_alter_module_owners"),
    ]

    operations = [
        migrations.CreateModel(
            name="University",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="module",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="studentuser",
            name="email",
        ),
        migrations.AddField(
            model_name="studentmodule",
            name="survey_status",
            field=models.CharField(
                choices=[("NOT_STARTED", "Not Started"), ("COMPLETED", "Completed")],
                default="NOT_STARTED",
                max_length=20,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "university_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.university",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="module",
            name="faculty",
        ),
        migrations.RemoveField(
            model_name="module",
            name="institution",
        ),
        migrations.RemoveField(
            model_name="module",
            name="module_id",
        ),
        migrations.AddField(
            model_name="user",
            name="university_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.university",
            ),
        ),
    ]
