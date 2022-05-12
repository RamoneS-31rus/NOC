from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class VlanNumber(models.Model):
    number = models.CharField(max_length=4, verbose_name='Номер')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.number}'


class Vlan(models.Model):
    number = models.ForeignKey(VlanNumber, on_delete=models.CASCADE, related_name='vlan', verbose_name='Номер')
    client = models.CharField(max_length=30, blank=True, verbose_name='Заказчик')
    used_for = models.CharField(max_length=50, blank=True, verbose_name='Назначение')
    point_a = models.CharField(max_length=30, blank=True, verbose_name='Точка А')
    point_b = models.CharField(max_length=30, blank=True, verbose_name='Точка Б')
    order = models.CharField(max_length=10, blank=True, verbose_name='Номер заказа')
    speed = models.IntegerField(default=0, verbose_name='Скорость (Mbps)')
    note = models.TextField(blank=True, verbose_name='Примечание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Изменил')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.number}'


class VlanHistory(models.Model):
    number = models.CharField(max_length=4, verbose_name='Номер')
    client = models.CharField(max_length=30, blank=True, verbose_name='Заказчик')
    used_for = models.CharField(max_length=50, blank=True, verbose_name='Назначение')
    point_a = models.CharField(max_length=30, blank=True, verbose_name='Точка А')
    point_b = models.CharField(max_length=30, blank=True, verbose_name='Точка Б')
    order = models.CharField(max_length=10, blank=True, verbose_name='Номер заказа')
    speed = models.CharField(max_length=5, verbose_name='Скорость (Mbps)')
    note = models.TextField(blank=True, verbose_name='Примечание')
    user = models.CharField(max_length=30, verbose_name='Изменил')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    status = models.BooleanField(null=True)  # None - create, False - delete, True - update

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.number}'


class Switch(models.Model):
    order = models.IntegerField(unique=True, verbose_name='Номер')
    address = models.CharField(max_length=50, blank=True, verbose_name='Адрес')
    ip = models.CharField(max_length=15, unique=True, verbose_name='IP')
    mac = models.CharField(max_length=17, unique=True, verbose_name='MAC')
    model = models.CharField(max_length=30, blank=True, verbose_name='Модель')
    firmware = models.CharField(max_length=30, blank=True, verbose_name='Прошивка')
    serial = models.CharField(max_length=30, unique=True, verbose_name='Серийный номер')
    note = models.TextField(blank=True, verbose_name='Примечание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Изменил')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_broken = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.mac = self.mac.upper().replace('-', ':')
        super(Switch, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order}'


class SwitchHistory(models.Model):
    order = models.CharField(max_length=255, verbose_name='Номер')
    address = models.CharField(max_length=50, blank=True, verbose_name='Адрес')
    ip = models.CharField(max_length=15, verbose_name='IP')
    mac = models.CharField(max_length=17, verbose_name='MAC')
    model = models.CharField(max_length=30, blank=True, verbose_name='Модель')
    firmware = models.CharField(max_length=30, blank=True, verbose_name='Прошивка')
    serial = models.CharField(max_length=30, verbose_name='Серийный номер')
    note = models.TextField(blank=True, verbose_name='Примечание')
    user = models.CharField(max_length=30, verbose_name='Изменил')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    status = models.BooleanField(null=True)  # None - create, False - ---, True - update

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.order}'
