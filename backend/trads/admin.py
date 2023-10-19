from django.contrib import admin

from .models import Icon, Img, RequestedElementDefault, Section, Trad


class MultiDBModelAdmin(admin.ModelAdmin):
    using = "trad"

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


@admin.register(Trad)
class TradAdmin(MultiDBModelAdmin):
    model = Trad
    list_display = [
        "__str__",
        "section",
        "fr_content",
        "fr_content_rich",
    ]
    search_fields = ("key", "fr_content", "fr_content_rich", "section__name")
    list_per_page = 10


@admin.register(Section)
class SectionAdmin(MultiDBModelAdmin):
    model = Section
    list_display = ["__str__"]


@admin.register(Icon)
class IconAdmin(MultiDBModelAdmin):
    model = Icon
    list_display = ["__str__"]
    search_fields = ("key", "link")


@admin.register(Img)
class ImgAdmin(MultiDBModelAdmin):
    model = Img
    list_display = ["__str__"]
    search_fields = ["key", "img_alt"]


@admin.register(RequestedElementDefault)
class RequestedElementDefaultAdmin(MultiDBModelAdmin):
    list_display = ["lang", "key", "value"]
    search_fields = ["lang", "key", "value"]
