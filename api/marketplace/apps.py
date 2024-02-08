from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.marketplace'

    def ready(self):
        import api.marketplace.signals  
