from django_filters import FilterSet, CharFilter, ChoiceFilter, ModelChoiceFilter
from .models import House
from addressbook.models import Address


class HouseFilter(FilterSet):
    # area = CharFilter(field_name='area__name', lookup_expr='icontains', label='Зона')
    # area = ModelChoiceFilter(field_name='area__name', widget=Select(attrs={'class': 'form-control mb-2'}))
    address = CharFilter(field_name='address__address_name', lookup_expr='icontains', label='Адрес')
    status = ChoiceFilter(field_name='status', choices=House.type, label='Статус ВОЛС')
