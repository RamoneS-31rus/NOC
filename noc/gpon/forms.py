from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.contrib.admin import widgets
from django.db.models import Q

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
    """переопределяем формат ввода даты"""
    date_con = forms.DateTimeField(
        required=False,
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 22.01.2021 14:00',
                                          'size': 25,
                                          }),
    )

    def __init__(self, *args, **kwargs):
        super(RequestFormCreate, self).__init__(*args, **kwargs)
        self.fields['router'].queryset = Product.objects.filter(type__type_name="Роутеры")
        self.fields['ont'].queryset = Product.objects.filter(type__type_name="Оптические терминалы")

    class Meta:
        model = Request
        fields = ['name', 'phone', 'date_con', 'tariff', 'ont', 'router', 'note']

        widgets = {
            'name': forms.TextInput(attrs={'size': 55}),
            'phone': forms.TextInput(attrs={'size': 27}),
            #     'date_con': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            # 'date_con': forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 2021-12-22 14:00',
            #                                        'size': 25,
            #                                        }),
            'note': forms.Textarea(attrs={'cols': 45,
                                          'rows': 2,
                                          }),
        }


class RequestFormUpdate(forms.ModelForm):
    """переопределяем формат ввода и вывода даты"""
    date_con = forms.DateTimeField(
        required=False,
        # input_formats=['%d.%m.%Y %H:%M'],
        # widget=forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 22.01.2021 14:00',
        #                                   'size': 25,
        #                                   },
        #                            format='%d.%m.%Y %H:%M')
        # initial=str(datetime.now().date()) + 'T10:00',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                          'size': 25,
                                          },)
                                   # format='%d.%m.%Y %H:%M')
    )
    # date_con = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
    # date_field = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    #                                  initial=format(datetime.date.today(), '%Y-%m-%dT%H:%M'), localize=True)

    def __init__(self, *args, **kwargs):
        super(RequestFormUpdate, self).__init__(*args, **kwargs)
        self.fields['installer'].queryset = User.objects.filter(groups__name='Installers', is_active=True).order_by('last_name')
        # self.fields['manager'].queryset = User.objects.filter(groups__name='Managers', is_active=True).order_by('last_name')
        self.fields['installer'].label_from_instance = lambda obj: "%s %s" % (obj.last_name, obj.first_name)
        # self.fields['manager'].label_from_instance = lambda obj: "%s %s" % (obj.last_name, obj.first_name)
        self.fields['router'].queryset = Product.objects.filter(type__type_name="Роутеры")
        self.fields['ont'].queryset = Product.objects.filter(type__type_name="Оптические терминалы")
        self.fields['cord'].queryset = Product.objects.filter(Q(type__type_name="Оптические патч-корды") | Q(type__type_name="Оптический кабель"))
        """Если date_con есть, то переопределяем формат полученной даты на '2022-12-30T10:00' для datetime-local"""
        if self.initial['date_con']:
            self.initial['date_con'] = (self.initial['date_con'] + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Request
        fields = ['name', 'phone', 'date_con', 'tariff', 'ont', 'router', 'cord', 'whose_cord', 'discount', 'installer', 'note']

        widgets = {
            'name': forms.TextInput(attrs={'size': 25}),
            'phone': forms.TextInput(attrs={'size': 12}),
            #     'date_con': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            # 'date_con': forms.DateTimeInput(attrs={'placeholder': 'формат ввода: 2021-12-22 14:00',
            #                                        'size': 25,
            #                                        },
            #                                 format='%d.%m.%Y %H:%M'),
            'discount': forms.TextInput(attrs={'size': 4}),
            'installer': forms.CheckboxSelectMultiple(),
            # 'manager': forms.Select(),
            'note': forms.Textarea(attrs={'cols': 45,
                                          'rows': 2,
                                          }),
        }

# class EventSplitDateTime(forms.SplitDateTimeWidget):
#     def __init__(self, attrs=None):
#         widgets = [forms.TextInput(attrs={'class': 'vDateField'}),
#                    forms.TextInput(attrs={'class': 'vTimeField'})]
#         # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
#         # we want to define widgets.
#         forms.MultiWidget.__init__(self, widgets, attrs)
#
#     def format_output(self, rendered_widgets):
#         return mark_safe(u'%s<br />%s' % (rendered_widgets[0], rendered_widgets[1]))
#
# class EventForm(forms.Form):
#     start = forms.DateTimeField(label=ugettext("Start"), widget=EventSplitDateTime())
#     end = forms.DateTimeField(label=ugettext("End"), widget=EventSplitDateTime())