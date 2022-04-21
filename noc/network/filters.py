from django.db.models import Q
from django.forms import TextInput
from django_filters import FilterSet, CharFilter
from .models import Vlan, Switch

import re


class VlanFilter(FilterSet):
    vlan_name = CharFilter(label='Vlan', field_name='vlan_name', lookup_expr='exact')
    vlan_client = CharFilter(label='Заказчик', field_name='vlan_client', lookup_expr='icontains')
    vlan_order = CharFilter(label='Номер заказа', field_name='vlan_order', lookup_expr='exact')
    vlan_used_for = CharFilter(label='Назначение', field_name='vlan_used_for', lookup_expr='icontains')


class SwitchFilter(FilterSet):
    # address = filters.CharFilter(label='Адрес', field_name='address', lookup_expr='icontains')
    # ip = filters.CharFilter(label='IP', field_name='ip', lookup_expr='exact')
    # mac = filters.CharFilter(label='', field_name='mac', lookup_expr='icontains')
    # model = filters.CharFilter(label='Модель', field_name='model', lookup_expr='icontains')
    switch = CharFilter(label='', method='search', widget=TextInput(attrs={'placeholder': 'Поиск'}))

    def search(self, queryset, name, value):
        ipv4_re = (
            r"(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)"
            r"(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}"
        )
        mac_re = (
            r'(?:[0-9a-fA-F]{2})'
            r'(?:(\:|\-)(?:[0-9a-fA-F]{2})){5}'
        )

        if re.match(ipv4_re, value):
            return Switch.objects.filter(ip=value)
        elif re.match(mac_re, value):
            value = value.upper().replace('-', ':')
            return Switch.objects.filter(mac=value)
        else:
            return Switch.objects.filter(
                Q(address__icontains=value) | Q(model=value) | Q(serial=value))


        # if len(value) < 2:
        #     return House.objects.filter(Q(address__address_name__icontains=value[0]) | Q(address__address_house=value[0]))
        # return House.objects.filter(Q(address__address_name__icontains=value[0]) & Q(address__address_house=value[1]))
