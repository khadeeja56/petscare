from django.core.management.base import BaseCommand
from scheduler.cron import send_reminders_cron

class Command(BaseCommand):
    help = 'Send appointment reminders'

    def handle(self, *args, **options):
        send_reminders_cron()
        self.stdout.write(self.style.SUCCESS('Reminders sent (if any).'))
