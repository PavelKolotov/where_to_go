from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Place, Image
from adminsortable2.admin import SortableAdminBase, SortableStackedInline



class ImageInline(SortableStackedInline):
    model = Image
    readonly_fields = ['preview', ]
    extra = 1


    def preview(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.image.url,
            height=200, )
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline, ]
    search_fields = ['title']






