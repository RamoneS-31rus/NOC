from django import forms
from django.db.models import Q
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFromToRangeFilter, BooleanFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
from django.contrib.auth.models import User
from django.forms import CheckboxInput

from .models import House, Request


class HouseFilter(FilterSet):
    address = CharFilter(method='address_filter')
    status = ChoiceFilter(field_name='status', choices=House.type, label='Статус ВОЛС')

    class Meta:
        model = House
        fields = ['address', 'district', 'status']

    def address_filter(self, queryset, name, value):
        value = value.split()  # разбиваем строку на список с элементами по одному слову
        if len(value) == 1 & value[0][-2:-1].isdigit():  # если ищем по номеру дома и в нем есть буква, дулаем её заглавной
            value = [value[0][:-1] + value[0][-1:].upper()]
        elif len(value) == 2:
            if value[0][:1:].isdigit():  # Если название двойное и начинается с числа, то объединяем в одно
                value = [value[0] + ' ' + value[1].capitalize()]
            elif value[1][:1:].isdigit():
                value[0] = value[0].capitalize()  # у первого слова делаем первую букву заглавную, а остнольные маленькие
                value[1] = value[1][:-1] + value[1][-1:].upper()  # у номера дома делаем букву заглавной, если она есть
            else:
                value = [value[0].capitalize() + ' ' + value[1].capitalize()]
        elif len(value) == 3:  # Если у улицы двойное название
            if value[0][:1:].isdigit():
                value[0] = value[0] + ' ' + value[1].capitalize()  # и начинается с числа (1-й Заводской), то объединяем в одно значение
                value[1] = value.pop().upper()  # Номер дома переносим с 3-й позиции на вторую
            else:
                value[0] = value[0].capitalize() + ' ' + value[1].capitalize()
                value[1] = value.pop().upper()
        else:
            value[0] = value[0].capitalize()
        """
        Если в списке один элемент, то фильтруем или по названию улицы, или по номеру дома.
        Если элементов больше одного, то фильтруем по названию и номеру.
        """
        if len(value) < 2:
            return House.objects.filter(Q(address__address_name__icontains=value[0]) | Q(address__address_house=value[0]))
        return House.objects.filter(Q(address__address_name__icontains=value[0]) & Q(address__address_house=value[1]))


class RequestFilter(FilterSet):
    date_con = DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    # installer = ModelChoiceFilter(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = Request
        fields = ['date_con']


# class StatisticFilter(FilterSet):
#     date_update = DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
#
#     class Meta:
#         model = Request
#         fields = ['date_update']


# class RequestHiddenFilter(FilterSet):
#     show_hidden = BooleanFilter(label='Показать скрытые заявки', method='hide_null', widget=CheckboxInput(attrs={}))
#
#     def hide_null(self, queryset, name, value):
#         if value:
#             return queryset.filter(Q(status='False', date_con__isnull=True) | Q(status__isnull=True)).order_by('-date_req')
#         else:
#             return queryset.filter(status='False', date_con__isnull=True).order_by('-date_req')

