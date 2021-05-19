from django.forms import ModelForm
from .models import Address, Contact


class AddressForm(ModelForm):

    class Meta:
        model = Address
        fields = ['name']


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'note']
