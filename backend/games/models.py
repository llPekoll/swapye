from django.db import models

from authie.models import UserAccount
from dash.models import GameType, Skin


class Game(models.Model):
    class TimeZone(models.TextChoices):
        Eu_Paris = "Europe/Paris"
        Us_Hawaii = "US/Hawaii"

    owner = models.ForeignKey(
        UserAccount,
        related_name="games",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    emblem = models.CharField(max_length=32, default="")
    link = models.CharField(max_length=255, default="")
    qr_location = models.CharField(max_length=255, default="")

    name = models.CharField(max_length=128)
    opening_text = models.CharField(max_length=255, null=True, blank=True)
    closing_text = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)

    game_type = models.ForeignKey(
        GameType, related_name="games", on_delete=models.CASCADE, null=True, blank=True
    )
    skin = models.ForeignKey(
        Skin, related_name="skins", on_delete=models.CASCADE, null=True, blank=True
    )

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    starting_time = models.TimeField(null=True, blank=True)
    ending_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    request_email = models.BooleanField(default=True)
    request_name = models.BooleanField(default=False)
    request_tel = models.BooleanField(default=False)
    request_address = models.BooleanField(default=False)
    unlimited_in_time = models.BooleanField(default=False)
    losing_factor = models.IntegerField(default=50)
    is_always_winner = models.BooleanField(default=False)
    can_replay = models.BooleanField(default=False)
    can_replay_today = models.BooleanField(default=False)

    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    insta = models.CharField(max_length=255, null=True, blank=True)

    timezone = models.CharField(
        max_length=128, choices=TimeZone.choices, default=TimeZone.Eu_Paris
    )

    force_result_won = models.BooleanField(default=False)
    force_result_lost = models.BooleanField(default=False)
    force_result_cant_replay = models.BooleanField(default=False)
    force_result_cant_replay_today = models.BooleanField(default=False)
    dry_run = models.BooleanField(default=False)

    use_qr_for_games = models.BooleanField(default=False)

    # Mode Salon
    fullscreen_btn = models.BooleanField(default=True)
    restart_btn = models.BooleanField(default=True)
    automatic_restart_activated = models.BooleanField(default=True)
    automatic_restart_counter_value = models.IntegerField(default=20)

    # defautls override
    logo_company = models.CharField(max_length=255, null=True, blank=True)
    sound_overide = models.CharField(max_length=255, null=True, blank=True)
    email_check_override = models.BooleanField(default=False)
    bg_ingame = models.CharField(max_length=255, null=True, blank=True)
    form_portrait = models.CharField(max_length=255, null=True, blank=True)
    form_landscape = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name


class Price(models.Model):

    name = models.CharField(max_length=32)
    img = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(default=10)
    game = models.ForeignKey(Game, related_name="prices", on_delete=models.CASCADE)
    display_price_name = models.BooleanField(default=True)
    offset_price_name = models.CharField(max_length=32, null=True, blank=True)
    email_template = models.CharField(max_length=128, null=True, blank=True)
    consolation_price = models.BooleanField(default=False)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.name}-----{self.game}"


class WinnableTimeRange(models.Model):
    price = models.ForeignKey(
        Price, related_name="winnalbe_time_range", on_delete=models.CASCADE
    )
    day = models.DateField(null=True, blank=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.price}"


class WinnedPrice(models.Model):
    game = models.ForeignKey(
        Game,
        related_name="winned_prices",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    price = models.ForeignKey(
        Price,
        related_name="winned_prices",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    creation_date = models.DateTimeField(auto_now=True)
    price_code = models.CharField(max_length=64, null=True, blank=True)
    unlock_link = models.CharField(max_length=255, null=True, blank=True)
    price_qrlocation = models.CharField(max_length=255, null=True, blank=True)
    price_taken = models.BooleanField(default=False)
    picked_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.price}"


class RefusedLead(models.Model):

    email = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class ValidatedEmail(models.Model):

    email = models.CharField(max_length=255, null=True, blank=True)
    game = models.ForeignKey(
        Game, related_name="validated_email", on_delete=models.CASCADE
    )
    bouncer_return = models.JSONField()
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Lead(models.Model):

    email = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    game = models.ForeignKey(Game, related_name="leads", on_delete=models.CASCADE)
    can_reveceive_email = models.BooleanField(default=True, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True)
    validated_email = models.OneToOneField(
        ValidatedEmail, on_delete=models.CASCADE, null=True, blank=True
    )
    price_won = models.ForeignKey(
        WinnedPrice,
        related_name="leads",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.email}"


class ExtraGameLanguage(models.Model):
    class Langues(models.TextChoices):
        FR = "🇫🇷 France"
        EN = "🇬🇧 Anglais"
        ES = "🇪🇸 Espagnol"
        IT = "🇮🇹 Italien"
        DE = "🇩🇪 Allemand"
        CN = "🇨🇳 Chinois"

    game = models.ForeignKey(
        Game, related_name="extra_langagues", on_delete=models.CASCADE
    )
    lang = models.CharField(max_length=32, choices=Langues.choices, default=Langues.EN)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "lang"], name="game_and_lang")
        ]

    def __str__(self):
        return f"{self.game}_{self.lang}"


class RequestedElement(models.Model):
    class HTMLTypes(models.TextChoices):
        INPUT = "Input"
        CHECKBOX = "Checkbox"

    is_active = models.BooleanField(default=True)
    game = models.ForeignKey(
        Game, related_name="requested_elements", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=255, null=True, blank=True)
    kind = models.CharField(
        max_length=32, choices=HTMLTypes.choices, default=HTMLTypes.INPUT
    )

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.key}"


class RequestedElementLead(models.Model):
    lead = models.ForeignKey(
        Lead,
        related_name="requested_elements",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requested_element = models.ForeignKey(
        RequestedElement,
        related_name="requested_elements_lead",
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.requested_element}_{self.lead}"


class RequestedElementTrads(models.Model):
    requested_element = models.ForeignKey(
        RequestedElement,
        related_name="requested_elements_lang",
        on_delete=models.CASCADE,
    )
    extra_game_language = models.ForeignKey(
        ExtraGameLanguage,
        related_name="requested_traductions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    wording = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.requested_element}_{self.extra_game_language}"


class GameTrads(models.Model):

    extra_game_language = models.ForeignKey(
        ExtraGameLanguage, related_name="game_traductions", on_delete=models.CASCADE
    )
    opening_text = models.CharField(max_length=255, null=True, blank=True)
    closing_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.extra_game_language}"


class PricesTrads(models.Model):

    extra_game_language = models.ForeignKey(
        ExtraGameLanguage, related_name="price_traductions", on_delete=models.CASCADE
    )
    price = models.ForeignKey(
        Price,
        related_name="price_traductions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    img = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.extra_game_language}"
