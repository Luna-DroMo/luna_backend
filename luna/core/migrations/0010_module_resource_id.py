# Generated by Django 4.2.5 on 2024-01-17 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_module_resource_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='resource_id',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
