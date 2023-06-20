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
        response.raise_for_status()

        place_payload = response.json()
        try:
            Place.objects.get(title=place_payload['title'])
        except Place.DoesNotExist:
            obj, created = Place.objects.get_or_create(
                title=place_payload['title'],
                description_short=place_payload['description_short'],
                description_long=place_payload['description_long'],
                coordinate_lng=place_payload['coordinates']['lng'],
                coordinate_lat=place_payload['coordinates']['lat']
            )

            for image_url in place_payload['imgs']:
                self.download_img(image_url, obj)

    def download_img(self, image_url, obj):
        response = requests.get(image_url)
        response.raise_for_status()

        filename = Path(urlparse(image_url).path).name
        Image.objects.create(
            place=obj,
            image=ContentFile(response.content, name=filename)
        )
