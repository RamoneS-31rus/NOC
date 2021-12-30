from django.apps import AppConfig


class GponConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gpon'

    def ready(self):
        import gpon.signals
