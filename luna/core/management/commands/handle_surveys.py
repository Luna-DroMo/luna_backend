from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Module, StudentModule, StudentSurvey


class Command(BaseCommand):
    help = "Generate new survey instances based on module configuration"

    def handle(self, *args, **options):

        StudentSurvey.objects.update(isActive=False)
        self.stdout.write(self.style.SUCCESS("All existing surveys set to inactive."))

        modules = Module.objects.all()
        current_day = timezone.now().weekday()

        for module in modules:
            if module.survey_days == current_day:
                start_date = timezone.now().date()
                end_date = start_date + timedelta(days=7)
                StudentSurvey.objects.create(
                    module=module,
                    start_date=start_date,
                    end_date=end_date,
                    survey_status=StudentSurvey.SurveyStatus.NOT_COMPLETED,
                    is_active=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Survey created for module: {module.name}")
                )
