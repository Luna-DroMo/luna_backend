from django_cron import CronJobBase, Schedule
import logging

logger = logging.getLogger(__name__)


class SurveyCronjob(CronJobBase):
    RUN_EVERY_MINS = 1  # Job runs every minute
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "survey_generation"

    def do(self):
        try:
            from django.core.management import call_command

            logger.info("Starting survey generation job.")
            call_command("handle_surveys")
            logger.info("Survey generation job completed successfully.")
        except Exception as e:
            logger.error(f"Error in survey generation job: {str(e)}")
