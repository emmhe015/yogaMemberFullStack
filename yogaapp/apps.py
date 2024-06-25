from django.apps import AppConfig


class StudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yogaapp'

class YogaappConfig(AppConfig):
    name = 'yogaapp'

    def ready(self):
        import yogaapp.signals