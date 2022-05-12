from django.db.models import Q
from django.forms import TextInput, CheckboxInput
from django_filters import FilterSet, CharFilter, BooleanFilter

import re

from .models import VlanNumber, Switch


class VlanFilter(FilterSet):
    vlan = CharFilter(label='', method='search', widget=TextInput(attrs={'placeholder': 'Поиск'}))
    hide = BooleanFilter(label='', method='hide_null', widget=CheckboxInput(attrs={'title': 'Показать свободные'}))
    # show = BooleanFilter(label='', lookup_expr='isnull', field_name='vlan__number', widget=CheckboxInput(attrs={'title': 'Показать свободные'}))

    def search(self, queryset, name, value):
        value = value.split()
        if len(value) < 2:
            if value[0][:1:].isdigit() & value[0][-1].isdigit():  # если первый и последний символ число
                return VlanNumber.objects.filter(Q(number=value[0]) | Q(vlan__order=value[0]))
            else:
                return VlanNumber.objects.filter(Q(vlan__client__icontains=value[0]) | Q(vlan__used_for__icontains=value[0]))
        else:
            value = value[0] + ' ' + value[1]
            return VlanNumber.objects.filter(vlan__used_for__icontains=value)

    def hide_null(self, queryset, name, value):
        if value:
            return queryset
        else:
            return queryset.filter(vlan__number__isnull=value)


class SwitchFilter(FilterSet):
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
