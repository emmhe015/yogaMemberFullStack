from django.apps import AppConfig


class StudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yogaapp'

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals