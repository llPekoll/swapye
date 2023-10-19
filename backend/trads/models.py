from ckeditor.fields import RichTextField
from django.db import models
from django.utils.timezone import now


class Section(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Trad(models.Model):

    section = models.ForeignKey(Section, related_name="trads", on_delete=models.CASCADE)
    key = models.CharField(max_length=32, unique=True)
    fr_content = models.CharField(max_length=255, blank=True)
    fr_content_rich = RichTextField(blank=True)
    en_content = models.CharField(max_length=255, blank=True)
    en_content_rich = RichTextField(blank=True)

    def __str__(self):
        return self.key


class Icon(models.Model):

    key = models.CharField(max_length=32, unique=True)
    link = models.TextField(default="")

    def __str__(self):
        return self.key


class Img(models.Model):

    section = models.ForeignKey(Section, related_name="imgs", on_delete=models.CASCADE)

    key = models.CharField(max_length=255, blank=True)
    screenshot = models.FileField(upload_to="web/img")
    img_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.key


class RequestedElementDefault(models.Model):
    class Langues(models.TextChoices):
        FR = "🇫🇷 France"
        EN = "🇬🇧 Anglais"
        ES = "🇪🇸 Espagnol"
        IT = "🇮🇹 Italien"
        DE = "🇩🇪 Allemand"
        CN = "🇨🇳 Chinois"

    lang = models.CharField(max_length=32, choices=Langues.choices, default=Langues.FR)
    key = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.key}"
