# Generated by Django 4.2.5 on 2024-05-31 11:31

from django.db import migrations, models
from django.db import connection


def delete_student_survey_and_reset_index(apps, schema_editor):
    StudentSurvey = apps.get_model("core", "StudentSurvey")
    StudentSurvey.objects.all().delete()

    # Reset the primary key sequence (assuming it's an auto-increment field)
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE core_studentsurvey_id_seq RESTART WITH 1;")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0038_remove_form_form_type"),
    ]

    operations = [
        migrations.RunPython(delete_student_survey_and_reset_index),
    ]
