# Generated by Django 4.2.5 on 2024-04-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0034_alter_studentsurvey_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentsurvey",
            name="survey_number",
            field=models.IntegerField(default=1, editable=False),
        ),
    ]
