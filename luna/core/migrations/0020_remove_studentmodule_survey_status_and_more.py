# Generated by Django 4.2.5 on 2024-03-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_studentsurvey_alter_module_survey_days_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentmodule",
            name="survey_status",
        ),
        migrations.AddField(
            model_name="studentsurvey",
            name="survey_status",
            field=models.CharField(
                choices=[
                    ("NOT_COMPLETED", "Not Completed"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_COMPLETED",
                max_length=20,
                null=True,
            ),
        ),
    ]
