from django.apps import AppConfig
from django.db.models.signals import post_save

class ReposterConfig(AppConfig):
    name = 'reposter'

    def ready(self):
        import reposter.signals
