from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Module, StudentSurvey, StudentModule
import logging
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate new survey and activate module instances"

    def handle(self, *args, **options):

        try:

            # Archive surveys whose end_date is today
            self.archive_expired_surveys()

            active_modules = Module.objects.filter(
                start_date__lte=timezone.now(), end_date__gte=timezone.now()
            )

            for module in active_modules:

                if module.status == Module.Status.INACTIVE:
                    module.status = Module.Status.ACTIVE
                    module.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Activated module: {module.name}")
                    )

            # Get the current day number, 1=Monday through 7=Sunday
            current_day = str(timezone.now().weekday() + 1)

            # Get all modules that have a survey day matching today
            modules_matching_today = Module.objects.filter(
                survey_days=current_day, status=Module.Status.ACTIVE
            )

            if not modules_matching_today.exists():
                logger.info("No modules matching today to update.")
                print("No modules matching today to update.")
                return  # Early exit with implicit success code

            for module in modules_matching_today:

                student_modules = StudentModule.objects.filter(
                    module=module
                ).select_related("student")

                if student_modules.exists():  # Check if any entries are found
                    print(
                        f"Found {student_modules.count()} student modules for {module.name}"
                    )
                else:
                    print(f"No student modules found for {module.id}")

                today = timezone.now().date()
                for student_module in student_modules:
                    active_surveys = StudentSurvey.objects.filter(
                        module=module,
                        student=student_module.student,
                        status=StudentSurvey.Status.ACTIVE,
                    )
                    # Check if there is an active survey with start_date as today
                    if active_surveys.filter(start_date=today).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f"Active survey already exists for module: {module.name} and student: {student_module.student} starting today"
                            )
                        )
                        continue  # Skip creating a new survey

                    start_date = timezone.now().date()
                    end_date = start_date + timedelta(days=7)

                    StudentSurvey.objects.create(
                        module=module,
                        student=student_module.student,
                        start_date=start_date,
                        end_date=end_date,
                        resolution=StudentSurvey.Resolution.NOT_COMPLETED,
                        status=StudentSurvey.Status.ACTIVE,
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"New active survey created for module: {module.name}"
                        )
                    )

                self.stdout.write(
                    self.style.SUCCESS("Survey update process completed.")
                )
        except Exception as e:
            print(e)

    def archive_expired_surveys(self):
        today = timezone.now().date()
        expired_surveys = StudentSurvey.objects.filter(
            end_date__lte=today, status=StudentSurvey.Status.ACTIVE
        )

        if expired_surveys.exists():
            count = expired_surveys.update(
                status=StudentSurvey.Status.ARCHIVED, content=json.dumps(data)
            )
            self.stdout.write(self.style.SUCCESS(f"Archived {count} expired surveys."))
        else:
            self.stdout.write(self.style.SUCCESS("No surveys to archive."))


data = [
    {"id": 0, "value": 0},
    {"id": 1, "value": 0},
    {"id": 2, "value": 0},
    {"id": 3, "value": 0},
    {"id": 4, "value": 0},
    {"id": 5, "value": 0},
    {"id": 6, "value": 0},
    {"id": 7, "value": 0},
    {"id": 8, "value": 0},
    {"id": 9, "value": 0},
    {"id": 10, "value": 0},
    {"id": 11, "value": 0},
    {"id": 14, "value": 0},
    {"id": 13, "value": 0},
    {"id": 12, "value": 0},
    {"id": 15, "value": 0},
    {"id": 16, "value": 0},
    {"id": 17, "value": 0},
    {"id": 18, "value": 0},
    {"id": 19, "value": 0},
    {"id": 20, "value": 0},
    {"id": 21, "value": 0},
    {"id": 23, "value": 0},
    {"id": 24, "value": 0},
    {"id": 25, "value": 0},
    {"id": 22, "value": 0},
]
