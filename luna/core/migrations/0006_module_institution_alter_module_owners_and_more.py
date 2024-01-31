# Generated by Django 4.2.5 on 2024-01-17 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_module_owners'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='institution',
            field=models.CharField(max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='owners',
            field=models.ForeignKey(limit_choices_to={'user_type': (2, 3)}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='module',
            unique_together={('module_id', 'faculty')},
        ),
    ]