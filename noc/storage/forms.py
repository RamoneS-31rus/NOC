from django.forms import ModelForm
from .models import Product, Income, Object


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'type', 'name', 'quality', 'price', 'description']


class IncomeForm(ModelForm):

    class Meta:
        model = Income
        fields = ['income_category', 'income_type', 'income_name', 'income_quality', 'income_note']


class ObjectForm(ModelForm):

    class Meta:
        model = Object
        fields = ['object_address', 'object_purpose']

# class ExpenseForm(ModelForm):
#
#     class Meta:
#         model = Expense
#         fields = ['address',
#                   'name',
#                   'quantity',
#                   'description',
#                   ]