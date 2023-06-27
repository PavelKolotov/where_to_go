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

        place_obj, created = Place.objects.get_or_create(
            title=place_payload['title'],
            coordinate_lng=place_payload['coordinates']['lng'],
            coordinate_lat=place_payload['coordinates']['lat'],
            defaults= {
                'description_short': place_payload.get('description_short', ''),
                'description_long': place_payload.get('description_long', ''),
            }
        )

        for image_url in place_payload.get('imgs', []):
            self.download_img(image_url, place_obj)

    def download_img(self, image_url, place_obj):
        response = requests.get(image_url)
        response.raise_for_status()

        filename = Path(urlparse(image_url).path).name
        Image.objects.create(
            place=place_obj,
            image=ContentFile(response.content, name=filename)
        )
