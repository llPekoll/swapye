from django.urls import path

from .views import (
    BackupAllAPIview,
    ExportPaulAPIview,
    GameValidatorAPIview,
    UnlockPriceAPIview,
)

urlpatterns = [
    path("backup/all", BackupAllAPIview.as_view()),
    path("pour/paul", ExportPaulAPIview.as_view()),
    path("unlock/price/<str:tiny>", UnlockPriceAPIview.as_view()),
    path("game/validator/<str:emblem>", GameValidatorAPIview.as_view()),
]
