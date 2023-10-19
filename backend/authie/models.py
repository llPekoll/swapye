import uuid
from email.policy import default

from django.db import models
from django.utils.timezone import now


class UserAccount(models.Model):
    class CustomerType(models.TextChoices):
        OFF = "Off"
        TRIAL = "Trial"
        BASIC = "Basic"
        PLUS = "Plus"
        PREMIUM = "Premium"

    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_type = models.CharField(
        max_length=128, choices=CustomerType.choices, default=CustomerType.TRIAL
    )

    def __str__(self):
        return self.email


class UserPersonalInfo(models.Model):
    owner = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, primary_key=True
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    conact_email = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    rib = models.CharField(max_length=64, blank=True, null=True)
    siret = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class MailingInfo(models.Model):
    class EmailProvider(models.TextChoices):
        MAILJET = "MailJet"
        Courier = "Courier"

    owner = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, primary_key=True
    )

    provider = models.CharField(
        max_length=128, choices=EmailProvider.choices, default=EmailProvider.MAILJET
    )
    apikey = models.CharField(max_length=255, blank=True, null=True)
    apipass = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.owner}"


class GameDefaults(models.Model):

    owner = models.OneToOneField(
        UserAccount, on_delete=models.CASCADE, primary_key=True
    )
    email_check = models.BooleanField(default=False)
    logo = models.CharField(max_length=255, blank=True, null=True)
    music = models.CharField(max_length=255, blank=True, null=True)
    regulation = models.TextField(default="")
    policy_rules = models.TextField(default="")

    def __str__(self):
        return f"{self.owner}"


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    expired_at = models.DateTimeField()

    def __str__(self):
        return self.token


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email


class Note(models.Model):
    owner = models.ForeignKey(
        UserAccount,
        related_name="notes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class FeaturesPermission(models.Model):

    name = models.CharField(max_length=255)

    trial = models.BooleanField(default=False)
    basic = models.BooleanField(default=False)
    plus = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name
