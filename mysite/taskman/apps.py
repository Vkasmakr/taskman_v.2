from django.apps import AppConfig


class TaskmanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskman'

    def ready(self):
        from .signals import save_profile
