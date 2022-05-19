from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse

from addressbook.models import Address
from storage.models import Product


class District(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return f'{self.name}'


class House(models.Model):
    cable = 'Нет кабеля'
    welding = 'Необходима сварка'
    ready = 'Готов к подключению'
    type = [(cable, 'Нет кабеля'), (welding, 'Необходима сварка'), (ready, 'Готов к подключению')]
    district = models.ForeignKey(District, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Район')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, unique=True, verbose_name='Адрес')
    status = models.CharField(max_length=20, choices=type, default=cable, verbose_name='Статус')
    note = models.TextField(blank=True, verbose_name='Примечание')
    time = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['address']
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return f'{self.address}'


class Tariff(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название тарифа')
    speed = models.IntegerField(default='100', verbose_name='Скорость Мбит/с')
    price = models.IntegerField(verbose_name='Стоимость тарифа')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return f'{self.name}'


class Request(models.Model):
    address = models.OneToOneField(House, on_delete=models.CASCADE, verbose_name='Адрес')
    name = models.CharField(max_length=50, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    date_req = models.DateField(auto_now_add=True, verbose_name='Дата заявки')
    date_con = models.DateTimeField(blank=True, null=True, verbose_name='Дата подключения')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Тариф')
    tariff_cost = models.IntegerField(default=0, verbose_name='Стоимость тарифа')
    ont = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='ont', verbose_name='Модель ONT')
    router = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='router', verbose_name='Модель Wi-Fi роутера')
    router_cost = models.IntegerField(default=0, verbose_name='Стоимость роутера')
    cord = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cord', verbose_name='Патч-корд')
    whose_cord = models.BooleanField(default=False, verbose_name='Абонентский')  # Если True, то патч абонента
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка')
    cost_con = models.PositiveIntegerField(default=0, verbose_name='Стоимость подключения')
    installer = models.ManyToManyField(User, blank=True, related_name='installer', verbose_name='Монтажники')
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='manager', verbose_name='Менеджер')
    note = models.TextField(blank=True, verbose_name='Примечание')
    status = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def update_price(self):  # Расчёт стоимости подключения в зависимости от тарифа и оборудования
        # self.cost_con = 0
        price_con_ont_1 = 6000
        price_con_ont_wifi = 7500

        # if self.router is None:
        #     price_router = 0
        # else:
        #     price_router = int(Product.objects.get(name=self.router).price)
        #
        # if self.tariff is None:
        #     price_tariff = 0
        # else:
        #     price_tariff = int(Tariff.objects.get(name=self.tariff).price)

        if str(self.ont) == 'HS8545M5':
            # self.cost_con = price_con_ont_wifi + price_router + price_tariff - int(str(self.discount))
            Request.objects.filter(pk=self.pk).update(cost_con=(price_con_ont_wifi + F('router_cost') +
                                                                F('tariff_cost') - F('discount')))
        elif self.ont is not None and str(self.ont) != 'HS8545M5':
            # self.cost_con = price_con_ont_1 + price_router + price_tariff - int(str(self.discount))
            Request.objects.filter(pk=self.pk).update(cost_con=(price_con_ont_1 + F('router_cost') +
                                                      F('tariff_cost') - F('discount')))
        elif self.ont is None:
            pass
        # self.save()
        # from django.db.models import F
        # Profile.objects.select_for_update().filter(pk=self.pk).update(balance=F('balance') + 1)  # ПРИМЕР

    def save(self, *args, **kwargs):  # Изменение формата телефоннтого номера
        if self.phone != '':
            chars = ['+', '-', '.', '(', ')', ' ']
            for c in chars:
                if c in self.phone:
                    self.phone = self.phone.replace(c, "")
            # self.phone = self.phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('.', '')
            if len(self.phone) == 6:
                self.phone = self.phone[0:2] + '-' + self.phone[2:4] + '-' + self.phone[4:7]
            else:
                self.phone = self.phone[0] + ' (' + self.phone[1:4] + ') ' + self.phone[4:7] + '-' + self.phone[7:9] + '-' + self.phone[9:11]
        super(Request, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.address}'
