# Generated by Django 4.2.5 on 2024-01-17 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_module_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='resource_id',
        ),
    ]