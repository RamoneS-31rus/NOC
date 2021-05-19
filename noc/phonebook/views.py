from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Address, Contact
from .forms import AddressForm, ContactForm


class AddressList(ListView):
    model = Address
    template_name = 'phonebook/address_list.html'
    context_object_name = 'address_list'


class AddressDetail(DetailView):
    model = Address
    template_name = 'phonebook/address_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_detail'] = Address.objects.get(slug=self.kwargs.get('slug'))
        context['contact_list'] = Contact.objects.filter(address=Address.objects.get(
            slug=self.kwargs.get('slug')))
        return context

    # def get_success_url(self):
    #     return reverse('address_detail', kwargs={'slug': self.get_object().slug})
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form, **kwargs):
#         expense = form.save(commit=False)
#         expense.expense_user = self.request.user
#         expense.expense_address = self.get_object()
#         expense.save()
#         return super().form_valid(form)
#
#
class AddressCreate(CreateView):
    model = Address
    template_name = 'phonebook/address_form.html'
    form_class = AddressForm


class AddressUpdate(UpdateView):
    model = Address
    template_name = 'phonebook/address_form.html'
    form_class = AddressForm
    success_url = '/contacts/addresses/'


class AddressDelete(DeleteView):
    model = Address
    template_name = 'phonebook/delete.html'
    success_url = '/contacts/addresses/'


class ContactCreate(CreateView):
    model = Contact
    template_name = 'phonebook/contact_form.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('address_detail', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        contact = form.save(commit=False)
        contact.address_id = Address.objects.get(slug=self.kwargs['slug']).pk
        contact.save()
        return super().form_valid(form)


class ContactUpdate(UpdateView):
    model = Contact
    template_name = 'phonebook/contact_form.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('address_detail', kwargs={'slug': self.kwargs['slug']})

class ContactDelete(DeleteView):
    model = Contact
    template_name = 'phonebook/delete.html'

    def get_success_url(self):
        return reverse('address_detail', kwargs={'slug': self.kwargs['slug']})