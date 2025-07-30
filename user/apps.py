from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from user.signals import create_user,cutomuser_pre_delete,create_user_profile,save_user_profile








