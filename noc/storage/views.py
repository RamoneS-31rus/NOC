from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Product, Income, Object, Expense
from .forms import ProductForm, IncomeForm, ObjectForm, ExpenseForm


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'storage/product_list.html'


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'storage/product_detail.html'


class ProductCreate(CreateView):
    model = Product
    template_name = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class IncomeList(ListView):
    model = Income
    context_object_name = 'income_list'
    template_name = 'storage/income_list.html'


class IncomeCreate(CreateView):
    model = Income
    template_name = 'storage/income_form.html'
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
    template_name = 'storage/income_form.html'
    form_class = IncomeForm
    success_url = '/storage/income/'


class IncomeDelete(DeleteView):
    model = Income
    template_name = 'storage/income_delete.html'
    success_url = '/storage/income/'


class ObjectList(ListView):
    model = Object
    template_name = 'storage/object_list.html'
    context_object_name = 'object_list'


class ObjectDetail(FormMixin, DetailView):
    model = Object
    template_name = 'storage/object_detail.html'
    context_object_name = 'object'
    form_class = ExpenseForm
    expense_status = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_list'] = Expense.objects.filter(expense_address=Object.objects.get(
            slug=self.kwargs.get('slug')))
        return context

    def get_success_url(self):
        return reverse('object_detail', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        expense = form.save(commit=False)
        expense.expense_user = self.request.user
        expense.expense_address = self.get_object()
        expense.save()
        return super().form_valid(form)


class ObjectCreate(CreateView):
    model = Object
    template_name = 'storage/object_form.html'
    form_class = ObjectForm


class ObjectUpdate(UpdateView):
    model = Object
    template_name = 'storage/object_form.html'
    form_class = ObjectForm
    success_url = '/storage/objects/'


class ObjectDelete(DeleteView):
    model = Object
    template_name = 'storage/object_delete.html'
    success_url = '/storage/objects/'


class RedirectToPreviousMixin:  # миксин для редиректа на предыдущию страницу

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class ExpenseCreate(CreateView):
    model = Expense
    template_name = 'storage/expense_form.html'
    form_class = ExpenseForm


class ExpenseUpdate(RedirectToPreviousMixin, UpdateView):
    model = Expense
    template_name = 'storage/expense_form.html'
    form_class = ExpenseForm


class ExpenseDelete(RedirectToPreviousMixin, DeleteView):
    model = Expense
