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
    switch_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    switch_order = models.IntegerField(unique=True, verbose_name='Номер')
    switch_address = models.CharField(max_length=20, blank=True, verbose_name='Адрес')
    switch_ip = models.CharField(max_length=15, unique=True, verbose_name='IP')
    switch_mac = models.CharField(max_length=50, unique=True, verbose_name='MAC')
    switch_model = models.CharField(max_length=20, blank=True, verbose_name='Модель')
    switch_firmware = models.CharField(max_length=20, blank=True, verbose_name='Прошивка')
    switch_serial = models.CharField(max_length=20, unique=True, verbose_name='Серийный номер')
    switch_note = models.TextField(blank=True, verbose_name='Примечание')
    switch_time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    switch_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.switch_mac = self.switch_mac.upper().replace('-', ':')
        super(Switch, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('switch_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.switch_order}'


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
    switch_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    switch_order = models.ForeignKey(Switch, on_delete=models.CASCADE, verbose_name='Номер')  # TODO Изменить на OneToOne!!!
    switch_address = models.CharField(max_length=20, blank=True, verbose_name='Адрес')
    switch_ip = models.CharField(max_length=15, verbose_name='IP')
    switch_mac = models.CharField(max_length=50, verbose_name='MAC')  # TODO Убрать!!!
    switch_model = models.CharField(max_length=20, blank=True, verbose_name='Модель')  # TODO Убрать!!!
    switch_firmware = models.CharField(max_length=20, blank=True, verbose_name='Прошивка')
    switch_serial = models.CharField(max_length=20, verbose_name='Серийный номер')  # TODO Убрать!!!
    switch_note = models.TextField(blank=True, verbose_name='Примечание')
    switch_time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['-switch_time']

    def __str__(self):
        return f'{self.switch_order}'
