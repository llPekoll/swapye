from django.contrib import admin

from .models import GameType, Skin


class SkinInline(admin.TabularInline):
    model = Skin


@admin.register(GameType)
class GameAdmin(admin.ModelAdmin):
    inlines = [
        SkinInline,
    ]


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    pass
