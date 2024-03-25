from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Module, StudentModule, StudentSurvey


class Command(BaseCommand):
    help = "Generate StudentSurvey instances weekly on the specified survey day"

    def calculate_next_survey_date(self, survey_day, last_survey_date=None):
        today = timezone.now().date()
        survey_day = int(survey_day) - 1

        if last_survey_date is None:
            last_survey_date = today
        days_until_next_survey = (survey_day - today.weekday() + 7) % 7
        if days_until_next_survey == 0 and (
            not last_survey_date or last_survey_date < today
        ):
            return today

        return today + timedelta(days=days_until_next_survey)

    def handle(self, *args, **kwargs):
        print("Creating student surveys for the week")
        for module in Module.objects.all():
            if module.start_date <= timezone.now().date() <= module.end_date:
                last_survey_date = (
                    StudentSurvey.objects.filter(module=module)
                    .order_by("-created_at")
                    .first()
                    .created_at.date()
                    if StudentSurvey.objects.filter(module=module).exists()
                    else None
                )
                next_survey_date = self.calculate_next_survey_date(
                    module.survey_days, last_survey_date
                )
                print(next_survey_date)
                if next_survey_date > timezone.now().date():
                    students = StudentModule.objects.filter(
                        module=module
                    ).select_related("student")
                    print(f"Found {students.count()} students for module {module.name}")
                    for student_module in students:
                        print(
                            f"Creating survey for student {student_module.student.user_id}"
                        )
                        StudentSurvey.objects.create(
                            name=f"Survey for {module.name} - {student_module.student.first_name}",
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            end_date=next_survey_date + timedelta(days=7),
                            module=module,
                            student=student_module.student,
                            content={},
                            survey_status=StudentSurvey.SurveyStatus.NOT_COMPLETED,
                        )
        self.stdout.write(
            self.style.SUCCESS("Successfully processed student surveys for the week.")
        )
