from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Product, Income


@receiver(pre_save, sender=Income)
def quality_update(sender, instance, **kwargs):
    if instance.pk is None:  # проверка на наличие в бд, если нет, сработало на создание нового объекта
        product = Product.objects.get(name=instance.income_name)
        product.quality = product.quality + instance.income_quality
        product.save()
    else:  # если есть, то сработало на редактирование имеющегося
        product = Product.objects.get(name=instance.income_name)
        old_quality = Income.objects.get(pk=instance.id).income_quality  # значение до изменения
        current_quality = instance.income_quality  # измененное значение
        if current_quality > old_quality:  # корректируем количество в зависимости от нового значения
            new_quality = current_quality - old_quality
            product.quality = product.quality + new_quality
        else:
            new_quality = old_quality - current_quality
            product.quality = product.quality - new_quality
        product.save()


@receiver(pre_delete, sender=Income)
def quality_delete(sender, instance, **kwargs):
    product = Product.objects.get(name=instance.income_name)
    income_quality = Income.objects.get(pk=instance.id).income_quality
    product.quality = product.quality - income_quality
    product.save()
