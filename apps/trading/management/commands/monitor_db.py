import logging
import threading
import time
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Monitor database connections and scheduler threads'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Monitoring interval in seconds (default: 30)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting database and scheduler monitoring (interval: {interval}s)')
        )
        
        while True:
            try:
                self.monitor_connections()
                self.monitor_scheduler_threads()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('Monitoring stopped'))
                break

    def monitor_connections(self):
        """Monitor database connections"""
        try:
            with connection.cursor() as cursor:
                # Lấy thông tin connections từ PostgreSQL
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_connections,
                        COUNT(CASE WHEN state = 'active' THEN 1 END) as active_connections,
                        COUNT(CASE WHEN state = 'idle' THEN 1 END) as idle_connections
                    FROM pg_stat_activity 
                    WHERE datname = %s
                """, [settings.DATABASES['default']['NAME']])
                
                result = cursor.fetchone()
                total, active, idle = result
                
                logger.info(f"DB Connections - Total: {total}, Active: {active}, Idle: {idle}")
                self.stdout.write(
                    f"[{time.strftime('%H:%M:%S')}] DB Connections - Total: {total}, Active: {active}, Idle: {idle}"
                )
                
        except Exception as e:
            logger.error(f"Error monitoring connections: {e}")

    def monitor_scheduler_threads(self):
        """Monitor scheduler threads"""
        try:
            # Đếm số threads đang chạy
            active_threads = threading.active_count()
            
            # Lấy thông tin về threads
            thread_names = [t.name for t in threading.enumerate()]
            
            logger.info(f"Scheduler Threads - Active: {active_threads}, Names: {thread_names}")
            self.stdout.write(
                f"[{time.strftime('%H:%M:%S')}] Scheduler Threads - Active: {active_threads}"
            )
            
        except Exception as e:
            logger.error(f"Error monitoring threads: {e}")
