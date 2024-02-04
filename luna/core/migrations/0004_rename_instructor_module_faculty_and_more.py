# Generated by Django 4.2.5 on 2024-01-17 15:26

import core.customFields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_form_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='instructor',
            new_name='faculty',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='title',
            new_name='module_id',
        ),
        migrations.AddField(
            model_name='module',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='module',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='owners',
            field=models.ForeignKey(limit_choices_to={'user_type': [2, 3]}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='module',
            name='survey_days',
            field=core.customFields.DayOfTheWeekField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Student'), (2, 'Lecturer'), (3, 'Admin')], default=1),
        ),
    ]
