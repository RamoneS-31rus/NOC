from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Vlan(models.Model):
    vlan_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    vlan_name = models.CharField(max_length=4, unique=True, verbose_name='Vlan')
    vlan_client = models.CharField(max_length=30, blank=True, verbose_name='Заказчик')
    vlan_order = models.CharField(max_length=10, blank=True, verbose_name='Номер заказа')
    vlan_used_for = models.CharField(max_length=50, blank=True, verbose_name='Назначение')
    vlan_point_a = models.CharField(max_length=20, blank=True, verbose_name='Точка А')
    vlan_point_b = models.CharField(max_length=20, blank=True, verbose_name='Точка Б')
    vlan_speed = models.IntegerField(default=0, verbose_name='Скорость (Mbps)')
    vlan_note = models.TextField(blank=True, verbose_name='Примечание')
    vlan_time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('vlan_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.vlan_name}'


class Switch(models.Model):
    order = models.IntegerField(unique=True, verbose_name='Номер')
    address = models.CharField(max_length=50, blank=True, verbose_name='Адрес')
    ip = models.CharField(max_length=15, unique=True, verbose_name='IP')
    mac = models.CharField(max_length=17, unique=True, verbose_name='MAC')
    model = models.CharField(max_length=20, blank=True, verbose_name='Модель')
    firmware = models.CharField(max_length=20, blank=True, verbose_name='Прошивка')
    serial = models.CharField(max_length=20, unique=True, verbose_name='Серийный номер')
    note = models.TextField(blank=True, verbose_name='Примечание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Изменил')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.mac = self.mac.upper().replace('-', ':')
        super(Switch, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('switch_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.order}'


class VlanHistory(models.Model):
    vlan_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    vlan_name = models.ForeignKey(Vlan, on_delete=models.CASCADE, verbose_name='Vlan')
    vlan_client = models.CharField(max_length=30, blank=True, verbose_name='Заказчик')
    vlan_order = models.CharField(max_length=10, blank=True, verbose_name='Номер заказа')
    vlan_used_for = models.CharField(max_length=50, blank=True, verbose_name='Назначение')
    vlan_point_a = models.CharField(max_length=20, blank=True, verbose_name='Точка А')
    vlan_point_b = models.CharField(max_length=20, blank=True, verbose_name='Точка Б')
    vlan_speed = models.IntegerField(default=0, verbose_name='Скорость (Mbps)')
    vlan_note = models.TextField(blank=True, verbose_name='Примечание')
    vlan_time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['-vlan_time']

    def __str__(self):
        return f'{self.vlan_name}'


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
    date = models.DateTimeField(verbose_name='Дата изменения')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.order}'
