# Generated by Django 4.2.5 on 2024-01-17 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_instructor_module_faculty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='owners',
            field=models.ForeignKey(limit_choices_to={'user_type': 2}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]