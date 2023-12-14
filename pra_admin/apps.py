from django.apps import AppConfig


class PraAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pra_admin'

    def ready(self):
        import pra_admin.signals
