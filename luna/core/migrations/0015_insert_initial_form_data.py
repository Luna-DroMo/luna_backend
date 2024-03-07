from django.db import migrations


def insert_form_data(apps, schema_editor):
    FormModel = apps.get_model('core', 'Form')

    forms_data = [
        {
            "name": "AIST",
            "form_type": "AIST",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Kognitive Fähigkeiten",
            "form_type": "COGNITIVE",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Internale-Externale-Kontrollüberzeugung",
            "form_type": "INTERNAL_EXTERNAL",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Fachwissenstest Mathematik",
            "form_type": "MATH",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Motivation",
            "form_type": "MOTIVATION",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Persönlichkeits-skala",
            "form_type": "PERSONALITY",
            "content": {
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        },
        {
            "name": "Panas",
            "form_type": "PANAS",
            "content": {
                "form_type": "EQ",
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse?"
                    }
                ]
            },
        }
    ]

    for form in forms_data:
        FormModel.objects.create(**form)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0014_remove_user_university_id_studentform_submitted_at'),
    ]

    operations = [
        migrations.RunPython(insert_form_data),
    ]
