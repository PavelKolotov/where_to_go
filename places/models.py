from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Заголовок', max_length=100, blank=True)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = HTMLField('Описание', blank=True)
    coordinate_lng = models.FloatField('Долгота', null=True)
    coordinate_lat = models.FloatField('Широта', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Image(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='media')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return f'{self.id} {self.place}'

