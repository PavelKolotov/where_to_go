from django.db import models


class Place(models.Model):
    title = models.CharField('Заголовок', max_length=100, blank=True)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = models.TextField('Описание', blank=True)
    coordinate_lng = models.FloatField('Долгота', null=True)
    coordinate_lat = models.FloatField('Широта', null=True)

    def __str__(self):
        return self.title
