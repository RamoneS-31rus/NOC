from django import forms
from django.contrib.auth.models import User
from .models import House, Request


class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = ['area', 'address', 'status', 'note']

        widgets = {
            # 'address': forms.TextInput(attrs={'size': 23}),
            'address': forms.Select(),
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
        self.fields['installer'].queryset = User.objects.all().filter(groups__name='Installers')
        self.fields['manager'].queryset = User.objects.all().filter(groups__name='Managers')

    class Meta:
        model = Request
        fields = ['name', 'phone', 'date_con', 'tariff', 'ont', 'router', 'installer', 'manager', 'note']

    # installers = []
    # for user in User.objects.all():
    #     if user.groups.filter(name='Installers').exists():
    #         installers.append(user)

        widgets = {
            #     'address': forms.Select(),
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
