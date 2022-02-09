from django.db.models import Q
from django_filters import FilterSet, CharFilter, ChoiceFilter, ModelChoiceFilter

from .models import House
from addressbook.models import Address


class HouseFilter(FilterSet):
    # area = CharFilter(field_name='area__name', lookup_expr='icontains', label='Зона')
    # area = ModelChoiceFilter(field_name='area__name', widget=Select(attrs={'class': 'form-control mb-2'}))
    # area = ModelChoiceFilter(queryset=Area.objects.all())
    # address = CharFilter(field_name='address__address_name', lookup_expr='icontains', label='Улица')
    address = CharFilter(method='custom_filter')
    status = ChoiceFilter(field_name='status', choices=House.type, label='Статус ВОЛС')

    class Meta:
        model = House
        fields = ['address', 'status']

    def custom_filter(self, queryset, name, value):
        value = value.split()  # Разбиваем строку на список с элементами по одному слову
        value[0] = value[0].capitalize()  # У мервого слова делаем первую букву заглавную, а остнольные маленькие
        """
        Если в списке один элемент, то фильтруем или по названию улицы, или по номеру дома.
        Если элементов больше одного, то фильтруем по названию и номеру.
        """
        if len(value) < 2:
            return House.objects.filter(Q(address__address_name__icontains=value[0]) | Q(address__address_house=value[0]))
        return House.objects.filter(Q(address__address_name__icontains=value[0]) & Q(address__address_house=value[1]))
