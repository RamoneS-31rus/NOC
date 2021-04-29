from django_filters import FilterSet, filters
from .models import Vlan, Switch


class VlanFilter(FilterSet):
    vlan_name = filters.CharFilter(label='Vlan', field_name='vlan_name', lookup_expr='exact')
    vlan_client = filters.CharFilter(label='Заказчик', field_name='vlan_client', lookup_expr='icontains')
    vlan_order = filters.CharFilter(label='Номер заказа', field_name='vlan_order', lookup_expr='exact')
    vlan_used_for = filters.CharFilter(label='Назначение', field_name='vlan_used_for', lookup_expr='icontains')


class SwitchFilter(FilterSet):
    switch_address = filters.CharFilter(label='Адрес', field_name='switch_address', lookup_expr='icontains')
    switch_ip = filters.CharFilter(label='IP', field_name='switch_ip', lookup_expr='exact')
    switch_mac = filters.CharFilter(label='MAC', field_name='switch_mac', lookup_expr='icontains')
    switch_model = filters.CharFilter(label='Модель', field_name='switch_model', lookup_expr='icontains')
