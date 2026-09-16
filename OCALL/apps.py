from django.apps import AppConfig

class OcallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "OCALL"
    def ready(self):
        import OCALL.signals