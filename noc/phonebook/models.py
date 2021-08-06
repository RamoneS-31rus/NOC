from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify


class Address(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super(Address, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('address_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name}'


class Contact(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес')
    name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    note = models.CharField(max_length=100, blank=True, verbose_name='Примечание')

    def __str__(self):
        return f'{self.address}'
