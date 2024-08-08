from django.apps import AppConfig


class UserauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauths'

class UsersConfig(AppConfig):
    name = 'userauths'

    def ready(self):
        import userauths.signals