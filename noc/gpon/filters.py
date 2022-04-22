from django.db.models import Q
from django_filters import FilterSet, CharFilter, ChoiceFilter

from .models import House


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
            else:
                value[0] = value[0].capitalize()  # у первого слова делаем первую букву заглавную, а остнольные маленькие
                value[1] = value[1][:-1] + value[1][-1:].upper()  # у номера дома делаем букву заглавной, если она есть
        elif len(value) == 3:
            value[0] = value[0] + ' ' + value[1].capitalize()  # Если у улицы двойное название (1-й Заводской), то объединяем в одно значение
            value[1] = value.pop()  # Номер дома переносим с 3-й позиции на вторую
        else:
            value[0] = value[0].capitalize()
        """
        Если в списке один элемент, то фильтруем или по названию улицы, или по номеру дома.
        Если элементов больше одного, то фильтруем по названию и номеру.
        """
        if len(value) < 2:
            return House.objects.filter(Q(address__address_name__icontains=value[0]) | Q(address__address_house=value[0]))
        return House.objects.filter(Q(address__address_name__icontains=value[0]) & Q(address__address_house=value[1]))
