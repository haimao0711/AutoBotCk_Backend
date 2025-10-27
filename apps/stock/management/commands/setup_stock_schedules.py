from django.core.management.base import BaseCommand
from apps.stock.scheduler.celery_scheduler import setup_stock_schedules
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Setup Stock data download schedules in Celery Beat database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Setting up Stock schedules...'))
        
        result = setup_stock_schedules()
        
        if result:
            self.stdout.write(self.style.SUCCESS('✅ Stock schedules setup completed!'))
            self.stdout.write('\nTo view schedules, check:')
            self.stdout.write('  - Django Admin: /admin/django_celery_beat/periodictask/')
            self.stdout.write('  - Flower: http://localhost:5555/')
        else:
            self.stdout.write(self.style.ERROR('❌ Failed to setup Stock schedules'))

