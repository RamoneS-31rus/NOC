from datetime import datetime

from django import forms
from .models import Category, Type, Product, Income, Object, Expense


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'category', 'type', 'name', 'quality', 'price', 'description']


class CustomSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            if name == 'category':
                option['attrs']['name'] = 'category' + '-' + str(value.instance.id)
            elif name == 'type':
                option['attrs']['name'] = 'category' + '-' + str(value.instance.type_category_id)
                option['attrs']['class'] = 'hide_obj'
            elif name == 'name':
                option['attrs']['name'] = 'type' + '-' + str(value.instance.type_id)
                option['attrs']['class'] = 'hide_obj'
        else:
            option['label'] = ' --- Выберите --- '
            option['attrs']['class'] = 'center'
        return option


class IncomeForm(forms.ModelForm):
    date_create = forms.DateField(initial=datetime.now().date(),
                                  widget=forms.DateInput(attrs={'type': 'date',
                                                                'style': 'float: right; width: 172px',
                                                                }),
                                  label='Дата')

    class Meta:
        model = Income
        fields = ['date_create', 'category', 'type', 'name', 'quality', 'note']
        widgets = {'category': CustomSelect(attrs={'style': 'float: right; width: 177px;',
                                                   'onchange': 'if (this.selectedIndex) isCategory(value)'
                                                   }),
                   'type': CustomSelect(attrs={'style': 'float: right; width: 177px;',
                                               'onchange': 'if (this.selectedIndex) isType(value)'
                                               }),
                   'name': CustomSelect(attrs={'style': 'float: right; width: 177px;'}),
                   'quality': forms.NumberInput(attrs={'style': 'float: right; width: 169px'}),
                   'note': forms.TextInput(attrs={'style': 'float: right; width: 171px;'})
                   }


# class IncomeForm(forms.ModelForm):
#     date_create = forms.DateField(initial=datetime.now().date(),
#                                   widget=forms.DateInput(attrs={'type': 'date',
#                                                                 'style': 'float: right; width: 172px',
#                                                                 }),
#                                   label='Дата')
#     category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={'style': 'float: right; width: 177px'}))
#     type = forms.ModelChoiceField(label='Тип', queryset=Type.objects.all(),
#                                   widget=forms.Select(attrs={'style': 'float: right; width: 177px'}))
#     name = forms.ModelChoiceField(label='Название', queryset=Product.objects.all(),
#                                   widget=forms.Select(attrs={'style': 'float: right; width: 177px'}))
#
#     class Meta:
#         model = Income
#         fields = ['date_create', 'category', 'type', 'name', 'quality', 'note']
#         widgets = {
#             'quality': forms.NumberInput(attrs={'style': 'float: right; width: 169px'}),
#             'note': forms.TextInput(attrs={
#                                            'style': 'float: right; width: 171px;',
#                                            })
#         }


class ObjectFormCreate(forms.ModelForm):
    date_create = forms.DateField(initial=datetime.now().date(),
                                  widget=forms.DateInput(attrs={'type': 'date'}),
                                  label='Дата')
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all())
    type = forms.ModelChoiceField(label='Тип', queryset=Type.objects.all())
    name = forms.ModelChoiceField(label='Название', queryset=Product.objects.all())
    quality = forms.IntegerField(label='Количество')

    class Meta:
        model = Object
        fields = ['date_create', 'address', 'purpose']


class ObjectFormUpdate(forms.ModelForm):

    class Meta:
        model = Object
        fields = ['date_create', 'address', 'purpose']
        widgets = {
            'date_create': forms.DateInput(attrs={'type': 'date',
                                                  'style': 'float: right; width: 175px'
                                                  }),
            'address': forms.TextInput(attrs={'style': 'float: right; width: 172px'}),
            'purpose': forms.TextInput(attrs={'style': 'float: right; width: 172px;'})
        }


class ExpenseForm(forms.ModelForm):
    # date_create = forms.DateField(initial=datetime.now().date(),
    #                               widget=forms.DateInput(attrs={'type': 'date'}),
    #                               label='Дата')

    class Meta:
        model = Expense
        fields = ['category', 'type', 'name', 'quality']
