from django import forms
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
        fields = ['switch_address', 'switch_ip', 'switch_mac', 'switch_model', 'switch_firmware',
                  'switch_serial', 'switch_note', 'switch_status']

        widgets = {
            'switch_address': forms.TextInput(attrs={'size': 23}),
            'switch_ip': forms.TextInput(attrs={'size': 10}),
            'switch_mac': forms.TextInput(attrs={'size': 13}),
            'switch_model': forms.TextInput(attrs={'size': 23}),
            'switch_firmware': forms.TextInput(attrs={'size': 23}),
            'switch_serial': forms.TextInput(attrs={'size': 23}),
            'switch_note': forms.Textarea(attrs={'rows': 1, 'cols': 109}),
            'switch_status': forms.CheckboxInput()
        }

        # widgets = {
        #     'switch_address': forms.TextInput(attrs={
        #         'size': '23',
        #         'class': 'form-control',
        #         'placeholder': 'Адрес'
        #     }),
        # }
