from django.contrib import admin
from .models import Place, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    fields = ['title', 'description_short', 'description_long', 'coordinate_lng', 'coordinate_lat']



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

