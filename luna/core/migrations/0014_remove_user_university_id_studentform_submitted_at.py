# Generated by Django 4.2.5 on 2024-02-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_alter_form_unique_together_form_created_by_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="university_id",
        ),
        migrations.AddField(
            model_name="studentform",
            name="submitted_at",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
