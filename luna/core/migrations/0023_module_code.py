# Generated by Django 4.2.5 on 2024-03-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_studentsurvey_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="module",
            name="code",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
