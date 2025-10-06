from django.apps import AppConfig

class VillageNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'village_news'
    
    def ready(self):
        import village_news.signals