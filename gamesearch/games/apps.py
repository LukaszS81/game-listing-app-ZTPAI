from django.apps import AppConfig


from django.apps import AppConfig

class GamesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'games'

    def ready(self):
        import games.models  

