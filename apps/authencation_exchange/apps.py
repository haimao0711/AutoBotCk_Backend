from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AuthencationExchangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authencation_exchange'
    
    def ready(self) -> None:
        logger.info('Automation Authencation Job')
        # from .scheduler import automation_authencation as authencation_job
        # authencation_job.start()
