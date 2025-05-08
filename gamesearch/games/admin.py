from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
    exclude = ['user']  

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Game, GameAdmin)
