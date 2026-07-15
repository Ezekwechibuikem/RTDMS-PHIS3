from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from accounts_profiles.models import UserProfile
import logging
import time

logger = logging.getLogger(__name__)


def run_leave_increment_job():
    profiles = UserProfile.objects.filter(user__is_active=True)
    count = 0
    for profile in profiles:
        profile.apply_increment()
        count += 1
    logger.info(f'Leave increment applied to {count} profiles.')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start():

    # Wait until Django has finished starting
    time.sleep(5)

    # Synchronize leave balances once
    run_leave_increment_job()

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        run_leave_increment_job,
        trigger=CronTrigger(day=1, hour=0, minute=0),
        id="run_leave_increment",
        replace_existing=True,
    )

    scheduler.start()