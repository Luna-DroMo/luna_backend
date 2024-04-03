from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Module, StudentSurvey


class Command(BaseCommand):
    help = "Generate new survey instances based on module configuration"

    def handle(self, *args, **options):

        # Get the current day number, 1=Monday through 7=Sunday
        current_day = timezone.now().weekday() + 1

        # Get all modules that have a survey day matching today
        modules_matching_today = Module.objects.filter(survey_days=current_day)

        for module in modules_matching_today:
            # Set all current surveys for the module to inactive
            StudentSurvey.objects.filter(module=module, is_active=True).update(
                is_active=False
            )

            # Create a new active survey instance for the module
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
                self.style.SUCCESS(
                    f"New active survey created for module: {module.name}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Survey update process completed."))
