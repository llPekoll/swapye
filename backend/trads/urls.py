from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from .views import game_trads, get_trad, game_langs

urlpatterns = [
    path("trads/<str:lang>/<str:section>", csrf_exempt(get_trad)),
    path("game/trads/<str:emblem>", csrf_exempt(game_trads)),
    path("game/langs/<str:emblem>", csrf_exempt(game_langs)),
]
