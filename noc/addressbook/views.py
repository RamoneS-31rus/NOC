from django.views.generic import CreateView

from .forms import AddressForm
from .models import Address


class AddressCreate(CreateView):
    model = Address
    template_name = 'addressbook/form.html'
    form_class = AddressForm
    success_url = '/gpon/houses/'
