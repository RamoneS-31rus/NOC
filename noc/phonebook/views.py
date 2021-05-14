from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Address, Contact
#from .forms import ProductForm, IncomeForm, ObjectForm, ExpenseForm


class AddressList(ListView):
    model = Address
    template_name = 'phonebook/address_list.html'
    context_object_name = 'address_list'


class AddressDetail(DetailView):
    model = Address
    template_name = 'phonebook/address_detail.html'
    context_object_name = 'address_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_list'] = Contact.objects.filter(address=Address.objects.get(
            slug=self.kwargs.get('slug')))
        return context

    def get_success_url(self):
        return reverse('object_detail', kwargs={'slug': self.get_object().slug})
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
# class ObjectCreate(CreateView):
#     model = Object
#     template_name = 'storage/object_form.html'
#     form_class = ObjectForm
#
#
# class ObjectUpdate(UpdateView):
#     model = Object
#     template_name = 'storage/object_form.html'
#     form_class = ObjectForm
#     success_url = '/storage/objects/'
#
#
# class ObjectDelete(DeleteView):
#     model = Object
#     template_name = 'storage/object_delete.html'
#     success_url = '/storage/objects/'
