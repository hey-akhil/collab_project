from django.apps import AppConfig
import signals

class ClientappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClientApp'

    def ready(self):
        import ClientApp.signals
