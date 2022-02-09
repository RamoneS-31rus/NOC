from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from addressbook.models import Address
from storage.models import Product


# class Area(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#
#     def __str__(self):
#         return f'{self.name}'


class House(models.Model):
    cable = 'Нет кабеля'
    welding = 'Необходима сварка'
    ready = 'Готов к подключению'
    type = [(cable, 'Нет кабеля'), (welding, 'Необходима сварка'), (ready, 'Готов к подключению')]
    # area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Зона')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, unique=True, verbose_name='Адрес')
    status = models.CharField(max_length=20, choices=type, default=cable, verbose_name='Статус')
    note = models.TextField(blank=True, verbose_name='Примечание')
    time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['address']
    #
    # def get_absolute_url(self):
    #     return reverse('vlan_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.address}'


class Tariff(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название тарифа')
    speed = models.IntegerField(default='100', verbose_name='Скорость Мбит/с')
    price = models.IntegerField(verbose_name='Стоимость тарифа')

    def __str__(self):
        return f'{self.name}'


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    address = models.ForeignKey(House, on_delete=models.CASCADE, related_name='request', verbose_name='Адрес')
    name = models.CharField(max_length=50, blank=True, verbose_name='ФИО')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    date_req = models.DateField(auto_now_add=True, verbose_name='Дата заявки')
    date_con = models.DateTimeField(blank=True, null=True, verbose_name='Дата подключения')
    price_con = models.IntegerField(default='6000', verbose_name='Цена подключения')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Тариф')
    ont = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='ont', verbose_name='Модель ONT')
    router = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='router', verbose_name='Модель Wi-Fi роутера')
    note = models.TextField(blank=True, verbose_name='Примечание')
    time = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    installer = models.ManyToManyField(User, blank=True, related_name='installer', verbose_name='Монтажники')
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='manager', verbose_name='Менеджер')
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.phone = self.phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('.', '')
        self.phone = self.phone[0] + ' (' + self.phone[1:4] + ') ' + self.phone[4:7] + '-' + self.phone[7:9] + '-' + self.phone[9:11]
        super(Request, self).save(*args, **kwargs)

    #
    # def get_absolute_url(self):
    #     return reverse('vlan_detail', kwargs={'pk': self.pk})
    #

    def __str__(self):
        return f'{self.name}'
