# from django.db.models.signals import pre_save, pre_delete
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from addressbook.models import Address
# from .models import House
# # from storage.models import Product, Income, Expense
#
#
# @receiver(post_save, sender=Address)
# def save(instance, created, **kwargs):
#     if created:
#         House.objects.create(address=Address.objects.get(id=instance.id))
#         return

# @receiver(pre_save, sender=Request)
# def expense_quality_update(sender, instance, **kwargs):
#     if instance.pk is None:
#         if instance.router is None:
#             return
#         else:
#             product = Product.objects.get(name=instance.router)
#             product.quality = product.quality - 1
#     else:
#         product = Product.objects.get(name=instance.router)
#         print('bolt')
#         print(instance.router)
#         # product = Product.objects.get(name=instance.router)
#         # product.quality = product.quality - expense_quality
#         # product.save()
#         print(product.quality)
#     # if instance.pk is None:  # проверка на наличие в бд, если нет, сработало на создание нового объекта
#     #     product = Product.objects.get(name=instance.expense_name)
#     #     product.quality = product.quality - instance.expense_quality
#     #     product.save()
#     # else:  # если есть, то сработало на редактирование имеющегося
#     #     product = Product.objects.get(name=instance.expense_name)
#     #     old_quality = Expense.objects.get(pk=instance.id).expense_quality  # значение до изменения
#     #     current_quality = instance.expense_quality  # измененное значение
#     #     if current_quality > old_quality:  # корректируем количество в зависимости от нового значения
#     #         new_quality = current_quality - old_quality
#     #         product.quality = product.quality - new_quality
#     #     else:
#     #         new_quality = old_quality - current_quality
#     #         product.quality = product.quality + new_quality
#     #     product.save()
