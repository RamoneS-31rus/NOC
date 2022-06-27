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
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.type_name}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    code = models.CharField(max_length=10, blank=True, verbose_name='Код')
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    image = models.ImageField(default='default.jpg')
    quality = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    description = models.CharField(max_length=100, blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = slugify(self.name).lower() + '-' + str(Product.objects.last().id + 1)
            self.slug = slugify(self.name).lower()
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name}'


class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    quality = models.IntegerField(default=0, verbose_name='Количество')
    note = models.CharField(max_length=50, blank=True, verbose_name='Примечание')
    date_create = models.DateField(verbose_name='Дата')
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Добавил')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['-date_create']

    def save(self, *args, **kwargs):
        if not self.slug:
            if not Income.objects.all():
                index = 0
            else:
                index = Income.objects.order_by('id').last().id
            self.slug = slugify(self.name.name).lower() + '-' + str(index + 1)
        super(Income, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Object(models.Model):
    address = models.CharField(max_length=50, verbose_name='Адрес')
    purpose = models.CharField(max_length=50, verbose_name='Назначение')
    date_create = models.DateField(verbose_name='Дата')
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Добавил')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['-date_create']

    def save(self, *args, **kwargs):
        if not self.slug:
            if not Object.objects.all():
                index = 0
            else:
                index = Object.objects.order_by('id').last().id
            self.slug = slugify(self.address).lower() + '-' + str(index + 1)
        super(Object, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('object_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.address}'


class Expense(models.Model):
    address = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='expense', verbose_name='Адрес')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название')
    quality = models.IntegerField(default=0, verbose_name='Количество')
    # slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         if not Income.objects.all():
    #             index = 0
    #         else:
    #             index = Income.objects.order_by('id').last().id
    #         self.slug = slugify(self.name.name).lower() + '-' + str(index + 1)
    #     super(Expense, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
