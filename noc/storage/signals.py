from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Product, Income, Expense


@receiver(pre_save, sender=Income)
def income_quality_update(sender, instance, **kwargs):
    if instance.pk is None:  # проверка на наличие в бд, если нет, сработало на создание нового объекта
        product = Product.objects.get(name=instance.name)
        product.quality = product.quality + instance.quality
        product.save()
    else:  # если есть, то сработало на редактирование имеющегося
        current_product = Product.objects.get(name=instance.name)  # измененное название
        old_product = Product.objects.get(name=Income.objects.get(pk=instance.id).name)  # старое название
        current_quality = instance.quality  # измененное значение
        old_quality = Income.objects.get(pk=instance.id).quality  # значение до изменения
        if current_product == old_product and current_quality != old_quality:
            if current_quality > old_quality:  # корректируем количество в зависимости от нового значения
                new_quality = current_quality - old_quality
                current_product.quality = current_product.quality + new_quality
            else:
                new_quality = old_quality - current_quality
                current_product.quality = current_product.quality - new_quality
        elif current_product != old_product:
            current_product.quality = current_product.quality + current_quality
            old_product.quality = old_product.quality - old_quality
            old_product.save()
        current_product.save()


@receiver(pre_delete, sender=Income)
def income_quality_delete(sender, instance, **kwargs):
    product = Product.objects.get(name=instance.name)
    income_quality = Income.objects.get(pk=instance.id).quality
    product.quality = product.quality - income_quality
    product.save()


# @receiver(pre_save, sender=Expense)
# def expense_quality_update(sender, instance, **kwargs):
#     if instance.pk is None:  # проверка на наличие в бд, если нет, сработало на создание нового объекта
#         product = Product.objects.get(name=instance.name)
#         product.quality = product.quality - instance.quality
#         product.save()
#     else:  # если есть, то сработало на редактирование имеющегося
#         product = Product.objects.get(name=instance.name)
#         old_quality = Expense.objects.get(pk=instance.id).quality  # значение до изменения
#         current_quality = instance.expense_quality  # измененное значение
#         if current_quality > old_quality:  # корректируем количество в зависимости от нового значения
#             new_quality = current_quality - old_quality
#             product.quality = product.quality - new_quality
#         else:
#             new_quality = old_quality - current_quality
#             product.quality = product.quality + new_quality
#         product.save()


# @receiver(pre_delete, sender=Expense)
# def expense_quality_delete(sender, instance, **kwargs):
#     product = Product.objects.get(name=instance.name)
#     expense_quality = Expense.objects.get(pk=instance.id).quality
#     product.quality = product.quality + expense_quality
#     product.save()
