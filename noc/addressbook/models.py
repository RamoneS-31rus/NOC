from django.db import models
from django.urls import reverse
from slugify import slugify


class Address(models.Model):
    avenue = 'проспект'
    street = 'улица'
    boulevard = 'бульвар'
    passage = 'проезд'
    lane = 'переулок'
    highway = 'шоссе'

    list = [(avenue, 'проспект'), (street, 'улица'), (boulevard, 'бульвар'), (passage, 'проезд'),
            (lane, 'переулок'), (highway, 'шоссе')]
    address_type = models.CharField(max_length=10, choices=list, default=street, verbose_name='Тип')
    address_name = models.CharField(max_length=50, verbose_name='Название')
    address_house = models.CharField(max_length=5, verbose_name='Номер дома')
    # slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    #
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.address_name).lower() + '-' + slugify(self.address_house).lower().replace(' ', '')
    #     super(Address, self).save(*args, **kwargs)
    #
    # def get_absolute_url(self):
    #     return reverse('address_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.address_type} {self.address_name} {self.address_house}'
