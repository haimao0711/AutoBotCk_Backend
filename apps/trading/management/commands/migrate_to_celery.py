from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.trading.scheduler.celery_scheduler import create_user_schedules, remove_user_schedules
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class Command(BaseCommand):
    help = 'Migrate from APScheduler to Celery'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be migrated without doing it')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write("DRY RUN MODE - No changes will be made")
        
        # Get all users with active schedulers
        users_with_scheduler = User.objects.filter(scheduler_status=True)
        
        self.stdout.write(f"Found {users_with_scheduler.count()} users with active schedulers")
        
        for user in users_with_scheduler:
            self.stdout.write(f"Processing user: {user.username}")
            
            if not dry_run:
                # Create Celery schedules
                success = create_user_schedules(user)
                if success:
                    self.stdout.write(f"✅ Created Celery schedules for {user.username}")
                else:
                    self.stdout.write(f"❌ Failed to create Celery schedules for {user.username}")
        
        self.stdout.write("Migration completed!")
