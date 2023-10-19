from django.contrib import admin

from .models import (
    ExtraGameLanguage,
    Game,
    GameTrads,
    Lead,
    Price,
    PricesTrads,
    RefusedLead,
    RequestedElement,
    RequestedElementLead,
    ValidatedEmail,
    WinnableTimeRange,
    WinnedPrice,
    RequestedElementTrads,
)


class ExtraGameLanguageInline(admin.TabularInline):
    model = ExtraGameLanguage


class PriceInline(admin.TabularInline):
    model = Price


class WinnableTimeRangeInline(admin.TabularInline):
    model = WinnableTimeRange


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "name",
        "game_type",
        "emblem",
    ]
    inlines = [
        PriceInline,
        ExtraGameLanguageInline,
    ]
    search_fields = ["name", "emblem"]
    readonly_fields = ["id"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["name", "game", "consolation_price", "number"]
    ordering = ("id",)
    inlines = [
        WinnableTimeRangeInline,
    ]


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    fields = ("email", "game", "creation_date", "price_won")

    raw_id_fields = ("price_won", "game")
    readonly_fields = ["creation_date", "nitty_gritty"]
    list_display = ["email", "prix_gagner", "game", "creation_date"]

    @admin.display(description="Price Won name")
    def nitty_gritty(self, obj):
        if obj.price_won:
            return obj.price_won.price.name
        return "no price won"

    @admin.display(empty_value="no price won")
    def prix_gagner(self, obj):
        if obj.price_won:
            return obj.price_won.price.name

    search_fields = ["game__emblem", "email"]


@admin.register(WinnedPrice)
class WinnedPriceAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_date"]
    list_display = [
        "price",
        "creation_date",
        "game",
    ]


@admin.register(RefusedLead)
class RefusedLeadAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_date"]
    list_display = ["email"]
    search_fields = ["game__id"]


@admin.register(GameTrads)
class GameTradsAdmin(admin.ModelAdmin):
    list_display = ["extra_game_language", "opening_text", "closing_text"]


@admin.register(RequestedElement)
class RequestedElementAdmin(admin.ModelAdmin):
    search_fields = ["game__emblem", "game__name"]
    list_display = ["key", "kind", "game", "is_active"]
    pass


@admin.register(RequestedElementLead)
class RequestedElementLead(admin.ModelAdmin):
    pass


@admin.register(RequestedElementTrads)
class RequestedElementTradsAdmin(admin.ModelAdmin):
    pass


@admin.register(PricesTrads)
class PricesTradsAdmin(admin.ModelAdmin):
    list_display = ["extra_game_language", "price", "name"]
    pass


@admin.register(ValidatedEmail)
class ValidatedEmailAdmin(admin.ModelAdmin):
    list_display = ["email", "get_owner", "game", "validated"]

    def get_owner(self, obj):
        return obj.game.owner

    get_owner.short_description = "Owner"

    readonly_fields = ["id"]
