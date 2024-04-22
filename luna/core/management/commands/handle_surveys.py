from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Module, StudentSurvey, StudentModule


class Command(BaseCommand):
    help = "Generate new survey and activate module instances"

    def handle(self, *args, **options):
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

        print(modules_matching_today)

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

            for student_module in student_modules:
                StudentSurvey.objects.filter(
                    module=module,
                    student=student_module.student,
                    status=StudentSurvey.Status.ACTIVE,
                ).update(status=StudentSurvey.Status.ARCHIVED)

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

            self.stdout.write(self.style.SUCCESS("Survey update process completed."))
