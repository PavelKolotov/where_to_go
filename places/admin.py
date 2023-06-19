from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image
from adminsortable2.admin import SortableAdminBase, SortableStackedInline


class ImageInline(SortableStackedInline):
    model = Image
    readonly_fields = ['preview', ]
    extra = 1

    def preview(self, image_obj):
        return format_html('<img src={} height={height}>', image_obj.image.url, height=200)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline, ]
    search_fields = ['title']
