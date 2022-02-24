from django.apps import AppConfig


class GponConfig(AppConfig):
    name = 'gpon'

    def ready(self):
        import gpon.signals
