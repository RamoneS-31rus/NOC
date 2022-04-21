from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

from .models import Vlan, Switch


class VlanForm(forms.ModelForm):

    class Meta:
        model = Vlan
        fields = ['vlan_client', 'vlan_order', 'vlan_used_for', 'vlan_point_a', 'vlan_point_b',
                  'vlan_speed', 'vlan_note']

        widgets = {
            'vlan_client': forms.TextInput(attrs={'size': 23}),
            'vlan_order': forms.TextInput(attrs={'size': 9}),
            'vlan_used_for': forms.TextInput(attrs={'size': 44}),
            'vlan_point_a': forms.TextInput(attrs={'size': 23}),
            'vlan_point_b': forms.TextInput(attrs={'size': 23}),
            'vlan_speed': forms.TextInput(attrs={'size': 5}),
            'vlan_note': forms.Textarea(attrs={'rows': 1, 'cols': 97})
        }


class SwitchForm(forms.ModelForm):

    class Meta:
        model = Switch
        fields = ['address', 'ip', 'mac', 'model', 'firmware',
                  'serial', 'note', 'status']
        error_messages = {
            'ip': {
                'unique': "Комутатор с таким IP уже существует!",
            },
            'mac': {
                'unique': "Комутатор с таким MAC уже существует!",
            },
            'serial': {
                'unique': "Комутатор с таким S/N уже существует!",
            },
        }

        widgets = {
            'address': forms.TextInput(attrs={'size': 30}),
            'ip': forms.TextInput(attrs={'size': 10}),
            'mac': forms.TextInput(attrs={'size': 13}),
            'model': forms.TextInput(attrs={'size': 23}),
            'firmware': forms.TextInput(attrs={'size': 23}),
            'serial': forms.TextInput(attrs={'size': 23}),
            'note': forms.Textarea(attrs={'rows': 1}),
            'status': forms.CheckboxInput()
        }
