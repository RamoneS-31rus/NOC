from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Income
from .forms import ProductForm, IncomeForm


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    templates = 'storage/product_list.html'


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    templates = 'storage/product_detail.html'


class ProductCreate(CreateView):
    model = Product
    templates = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class ProductUpdate(UpdateView):
    model = Product
    templates = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class IncomeList(ListView):
    model = Income
    context_object_name = 'income_list'
    templates = 'storage/income_list.html'


class IncomeCreate(CreateView):
    model = Income
    templates = 'storage/income_form.html'
    form_class = IncomeForm
    success_url = '/storage/income'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product = form.save(commit=False)
        product.income_user = self.request.user
        product.save()
        return redirect('income_list')


class IncomeUpdate(UpdateView):
    model = Income
    templates = 'storage/income_form.html'
    form_class = IncomeForm
    success_url = '/storage/income/'


class IncomeDelete(DeleteView):
    model = Income
    #templates = 'storage/income_delete.html'
    success_url = '/storage/income/'


# class ExpenseList(ListView):
#     model = Expense
#     template_name = 'storage/expense_list.html'
#     context_object_name = 'consumption_list'


# class ConsumptionUpdate(UpdateView):
#     model = ProductConsumption
#     form_class = ConsumptionForm
#     template_name = 'storage/expense_update.html'
