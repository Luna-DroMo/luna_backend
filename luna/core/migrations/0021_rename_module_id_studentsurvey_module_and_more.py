# Generated by Django 4.2.5 on 2024-03-20 11:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_remove_studentmodule_survey_status_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="studentsurvey",
            old_name="module_id",
            new_name="module",
        ),
        migrations.RenameField(
            model_name="studentsurvey",
            old_name="student_id",
            new_name="student",
        ),
    ]
