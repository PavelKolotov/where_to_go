import requests
from urllib.parse import urlparse
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Place, Image



class Command(BaseCommand):
    help = 'Добавляет экскурсионные места из json файлов'

    def add_arguments(self, parser):
        parser.add_argument('place', type=str, help='Введите путь к файлу с данными')

    def handle(self, *args, **kwargs):
        place = kwargs['place']
        response = requests.get(place)
        place_data = response.json()
        try:
            Place.objects.get(title=place_data['title'])
        except Place.DoesNotExist:
            obj, created = Place.objects.get_or_create(
                title=place_data['title'],
                description_short=place_data['description_short'],
                description_long=place_data['description_long'],
                coordinate_lng=place_data['coordinates']['lng'],
                coordinate_lat=place_data['coordinates']['lat']
            )

            for image_url in place_data['imgs']:
                self.download_img(image_url, obj)

    def download_img(self, image_url, obj):
        response = requests.get(image_url)
        response.raise_for_status()

        filename = Path(urlparse(image_url).path).name
        Image.objects.create(
            place=obj,
            image=ContentFile(response.content, name=filename)
        )


