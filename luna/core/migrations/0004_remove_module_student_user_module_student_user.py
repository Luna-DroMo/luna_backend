# Generated by Django 4.2.5 on 2023-12-05 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_studentuser_main_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='student_user',
        ),
        migrations.AddField(
            model_name='module',
            name='student_user',
            field=models.ManyToManyField(to='core.studentuser'),
        ),
    ]