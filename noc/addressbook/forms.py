from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Address
from gpon.models import District


class AddressForm(forms.ModelForm):
    district = forms.ModelChoiceField(queryset=District.objects.all())  # Поле для последующей передачи в объект House

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
        """Переопределяем вывод при ошибке дублирования"""
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Такой адрес уже существует!",
            }
        }

