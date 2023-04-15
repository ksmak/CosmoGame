from django.contrib import admin

from .models import (
    Game,
    Gamer,
    GameObject
)


admin.site.register(Game)
admin.site.register(Gamer)
admin.site.register(GameObject)
