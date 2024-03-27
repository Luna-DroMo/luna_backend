# Generated by Django 4.2.5 on 2024-03-27 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_university_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='owners',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('user_type', 2), ('user_type', 3), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
