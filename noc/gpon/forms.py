from django import forms
from django.contrib.auth.models import User

from .models import House, Request
from storage.models import Product


class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = ['status', 'note']

        widgets = {
            # 'address': forms.TextInput(attrs={'size': 23}),
            # 'address': forms.Select(),
            'status': forms.Select(),
            'note': forms.TextInput(attrs={'size': 44}),
        }


class RequestFormCreate(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['name', 'phone', 'date_con', 'tariff', 'ont', 'router', 'note']

        widgets = {
            'name': forms.TextInput(attrs={'size': 55}),
            'phone': forms.TextInput(attrs={'size': 27}),
            #     'date_con': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'date_con': forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 2021-12-22 14:00',
                                                   'size': 25,
                                                   }),
            'note': forms.Textarea(attrs={'cols': 45,
                                          'rows': 2,
                                          }),
        }


class RequestFormUpdate(forms.ModelForm):
    # date_con = forms.DateTimeField(
    #     label='Дата подключения',
    #     input_formats=['%d.%m.%Y %H:%M'],
    #     widget=forms.DateTimeInput()
    # )

    def __init__(self, *args, **kwargs):
        super(RequestFormUpdate, self).__init__(*args, **kwargs)
        self.fields['installer'].queryset = User.objects.filter(groups__name='Installers', is_active=True).order_by('last_name')
        self.fields['manager'].queryset = User.objects.filter(groups__name='Managers', is_active=True).order_by('last_name')
        self.fields['installer'].label_from_instance = lambda obj: "%s %s" % (obj.last_name, obj.first_name)
        self.fields['manager'].label_from_instance = lambda obj: "%s %s" % (obj.last_name, obj.first_name)
        self.fields['router'].queryset = Product.objects.filter(type__type_name="Роутеры")
        self.fields['ont'].queryset = Product.objects.filter(type__type_name="Оптические терминалы")

    class Meta:
        model = Request
        fields = ['name', 'phone', 'date_con', 'tariff', 'ont', 'router', 'installer', 'manager', 'note']

        widgets = {
            'name': forms.TextInput(attrs={'size': 25}),
            'phone': forms.TextInput(attrs={'size': 12}),
            #     'date_con': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'date_con': forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 2021-12-22 14:00',
                                                   'size': 25,
                                                   }),
            'installer': forms.CheckboxSelectMultiple(),
            'manager': forms.Select(),
            'note': forms.Textarea(attrs={'cols': 45,
                                          'rows': 2,
                                          }),
        }
