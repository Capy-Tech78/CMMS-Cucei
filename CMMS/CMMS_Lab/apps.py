from django.apps import AppConfig

class CmmsLabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CMMS_Lab'

    def ready(self):
        import CMMS_Lab.signals


