from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['preview', ]
    fields = ('image', 'preview', 'order')

    def preview(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.image.url,
            height=200, )
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]






