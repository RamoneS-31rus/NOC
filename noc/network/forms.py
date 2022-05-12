from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

from .models import Vlan, Switch


class VlanForm(forms.ModelForm):

    class Meta:
        model = Vlan
        fields = ['client', 'order', 'used_for', 'point_a', 'point_b',
                  'speed', 'note']

        widgets = {
            'client': forms.TextInput(attrs={'size': 23}),
            'order': forms.TextInput(attrs={'size': 9}),
            'used_for': forms.TextInput(attrs={'size': 44}),
            'point_a': forms.TextInput(attrs={'size': 23}),
            'point_b': forms.TextInput(attrs={'size': 23}),
            'speed': forms.TextInput(attrs={'size': 5}),
            'note': forms.Textarea(attrs={'rows': 1, 'cols': 97})
        }


class SwitchForm(forms.ModelForm):

    class Meta:
        model = Switch
        fields = ['address', 'ip', 'mac', 'model', 'firmware',
                  'serial', 'note']
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
            # 'is_broken': forms.CheckboxInput()
        }
