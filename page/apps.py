from django.apps import AppConfig



class PageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'page'


    def ready(self):
        from page.signals import slug_create

