from django.contrib import admin

from trads.admin import MultiDBModelAdmin

from .models import (
    FeaturesPermission,
    GameDefaults,
    MailingInfo,
    Note,
    Reset,
    UserAccount,
    UserPersonalInfo,
)


class NoteAdmin(admin.TabularInline):
    model = Note


@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        NoteAdmin,
    ]
    readonly_fields = ["uuid"]
    search_fields = ["email"]
    list_display = ["email", "customer_type", "uuid"]


@admin.register(MailingInfo)
class MailingInfoAdmin(admin.ModelAdmin):
    list_display = ["owner", "email"]


@admin.register(UserPersonalInfo)
class UserPersonalInfoAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "conact_email", "company_name"]


@admin.register(Reset)
class ResetAdmin(admin.ModelAdmin):
    pass


@admin.register(GameDefaults)
class GameDefaultAdmin(admin.ModelAdmin):
    list_display = ["owner", "email_check"]


@admin.register(FeaturesPermission)
class FeaturesPermissionAdmin(MultiDBModelAdmin):
    readonly_fields = ["name"]
    list_display = ["name", "trial", "basic", "plus", "premium"]
