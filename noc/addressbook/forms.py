from django import forms

from .models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['address_type', 'address_name', 'address_house']

        widgets = {
            'address_type': forms.Select(),
            'address_name': forms.TextInput(attrs={'placeholder': 'Название',
                                                   'size': 35}),
            'address_house': forms.TextInput(attrs={'placeholder': 'Номер дома',
                                                    'size': 7}),
        }
