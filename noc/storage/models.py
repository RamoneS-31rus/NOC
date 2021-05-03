from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Type(models.Model):
    type_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    type_name = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f'{self.type_name}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    # image = models.ImageField()
    quality = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    description = models.CharField(max_length=100, blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower() + '-' + str(Product.objects.last().id + 1)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name}'


class Income(models.Model):
    income_user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    income_type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    income_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    income_quality = models.IntegerField(default=0, verbose_name='Количество')
    income_note = models.CharField(max_length=50, blank=True, verbose_name='Примечание')
    income_date_create = models.DateTimeField(auto_now_add=True)
    income_date_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            if not Income.objects.last():
                index = 0
            else:
                index = Income.objects.last().id
            self.slug = slugify(self.income_name.name).lower() + '-' + str(index + 1)
        super(Income, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'


class Object(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=20, blank=True, verbose_name='Адрес')
    purpose = models.CharField(max_length=20, blank=True, verbose_name='Назначение')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.address).lower()
        super(Object, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('object_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.address}'


class Expense(models.Model):
    expense_user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    expense_type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    expense_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    expense_quality = models.IntegerField(default=0, verbose_name='Количество')
    expense_address = models.ForeignKey(Object, on_delete=models.CASCADE)
    expense_note = models.CharField(max_length=50, blank=True, verbose_name='Примечание')

    def __str__(self):
        return f'{self.expense_name}'
