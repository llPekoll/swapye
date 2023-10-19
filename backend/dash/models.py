from django.db import models

from authie.models import UserAccount


class GameType(models.Model):
    name = models.CharField(max_length=32, default="curtain")
    limited_users = models.ManyToManyField(UserAccount, blank=True)
    ref_id = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Skin(models.Model):
    name = models.CharField(max_length=32, default="Base")
    game = models.ForeignKey(GameType, related_name="skins", on_delete=models.CASCADE)
    limited_users = models.ManyToManyField(UserAccount, blank=True)
    ref_id = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "name"], name="game_and_name")
        ]

    def __str__(self):
        return f"{self.name}"
