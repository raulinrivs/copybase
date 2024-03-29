from django.apps import AppConfig


class CobrancaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cobranca'

    def ready(self):
        import config.celery