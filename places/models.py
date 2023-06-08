from django.db import models


class Place(models.Model):
    title = models.CharField('Заголовок', max_length=100, blank=True)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = models.TextField('Описание', blank=True)
    coordinate_lng = models.FloatField('Долгота', null=True)
    coordinate_lat = models.FloatField('Широта', null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='static/media')

    def __str__(self):
        return f'{self.id} {self.place}'
