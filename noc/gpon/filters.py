from django.db.models import Q
from django.forms import CheckboxInput
from django_filters import FilterSet, CharFilter, ChoiceFilter, BooleanFilter, ModelChoiceFilter

from .models import House
from addressbook.models import Address


class HouseFilter(FilterSet):
    # area = CharFilter(field_name='area__name', lookup_expr='icontains', label='Зона')
    # area = ModelChoiceFilter(field_name='area__name', widget=Select(attrs={'class': 'form-control mb-2'}))
    # area = ModelChoiceFilter(queryset=Area.objects.all())
    # address = CharFilter(field_name='address__address_name', lookup_expr='icontains', label='Улица')
    address = CharFilter(method='address_filter')
    status = ChoiceFilter(field_name='status', choices=House.type, label='Статус ВОЛС')
    # complete = BooleanFilter(method='complete_filter', widget=CheckboxInput, label='Завершенные')

    class Meta:
        model = House
        fields = ['address', 'status']

    def address_filter(self, queryset, name, value):
        value = value.split()  # разбиваем строку на список с элементами по одному слову
        if len(value) == 1 & value[0][-2:-1].isdigit():  # если ищем по номеру дома и в нем есть буква, дулаем её заглавной
            value = [value[0][:-1] + value[0][-1:].upper()]
        elif len(value) > 1:
            value[0] = value[0].capitalize()  # у первого слова делаем первую букву заглавную, а остнольные маленькие
            value[1] = value[1][:-1] + value[1][-1:].upper()  # у номера дома делаем букву заглавной, если она есть
        else:
            value[0] = value[0].capitalize()
        """
        Если в списке один элемент, то фильтруем или по названию улицы, или по номеру дома.
        Если элементов больше одного, то фильтруем по названию и номеру.
        """
        if len(value) < 2:
            return House.objects.filter(Q(address__address_name__icontains=value[0]) | Q(address__address_house=value[0]))
        return House.objects.filter(Q(address__address_name__icontains=value[0]) & Q(address__address_house=value[1]))

    # def complete_filter(self, queryset, name, value):
    #     if not value:
    #         return queryset.exclude(request__status=True)
    #     return queryset
