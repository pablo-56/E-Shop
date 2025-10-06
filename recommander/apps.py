from django.apps import AppConfig


class RecommanderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommander'

    def ready(self):
        from .views import train_model_init
        train_model_init() # Handle initial setup of model