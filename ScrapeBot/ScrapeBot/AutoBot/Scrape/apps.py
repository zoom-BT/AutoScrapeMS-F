from django.apps import AppConfig
from django.core.signals import request_finished
from django.dispatch import receiver

class ScrapeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AutoBot.Scrape'

    def ready(self):
        from .views import stop_scheduler  # Déplace l'import ici

        @receiver(request_finished)
        def shutdown_scheduler(sender, **kwargs):
            stop_scheduler()
