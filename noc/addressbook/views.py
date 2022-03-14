from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .forms import AddressForm
from .models import Address


class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'addressbook/form.html'
    form_class = AddressForm
    success_url = '/gpon/houses/'
