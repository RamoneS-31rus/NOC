from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .models import Product, Income, Object, Expense
from .forms import ProductForm, IncomeForm, ObjectFormCreate, ObjectFormUpdate, ExpenseForm


class RedirectToPreviousMixin:  # Миксин для редиректа на предыдущию страницу
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'storage/product_list.html'


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'storage/product_detail.html'


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'storage/product_form.html'
    form_class = ProductForm
    success_url = '/storage/catalog/'


class IncomeList(LoginRequiredMixin, ListView):
    model = Income
    # context_object_name = 'income_list'
    template_name = 'storage/income_list.html'


class IncomeCreate(LoginRequiredMixin, CreateView):
    model = Income
    template_name = 'storage/income_form_create.html'
    form_class = IncomeForm
    success_url = '/storage/income'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_create = self.request.user
        obj.save()
        return redirect('income_list')


class IncomeUpdate(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Income
    template_name = 'storage/income_form_update.html'
    form_class = IncomeForm


class IncomeDelete(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    model = Income


class ObjectList(LoginRequiredMixin, ListView):
    model = Object
    template_name = 'storage/object_list.html'
    context_object_name = 'object_list'


class ObjectCreate(LoginRequiredMixin, CreateView):
    model = Object
    template_name = 'storage/object_form_create.html'
    form_class = ObjectFormCreate

    def form_valid(self, form):
        obj = form.save(commit=False)
        category_id = self.request.POST['category']
        type_id = self.request.POST['type']
        name_id = self.request.POST['name']
        quality = self.request.POST['quality']
        obj.user_create = self.request.user
        obj.save()
        Expense.objects.create(address_id=Object.objects.order_by('id').last().id, category_id=category_id,
                               type_id=type_id, name_id=name_id, quality=quality)
        product = Product.objects.get(id=name_id)
        Product.objects.filter(id=name_id).update(quality=product.quality - int(quality))
        # slug = Object.objects.order_by('id').last().slug
        # return redirect('expense_add', slug)
        return redirect('object_list')


class ObjectUpdate(LoginRequiredMixin, UpdateView):
    model = Object
    template_name = 'storage/object_form_update.html'
    form_class = ObjectFormUpdate
    success_url = '/storage/objects/'


class ObjectDelete(LoginRequiredMixin, DeleteView):
    model = Object
    template_name = 'storage/object_delete.html'
    success_url = '/storage/objects/'


class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'storage/expense_form.html'
    form_class = ExpenseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.address_id = Object.objects.get(slug=self.kwargs.get('slug')).pk
        obj.save()
        product = Product.objects.get(name=obj.name)
        Product.objects.filter(name=obj.name).update(quality=product.quality - obj.quality)
        return redirect('object_list')


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expense

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        address_id = Object.objects.get(slug=self.kwargs.get('slug')).pk
        if Expense.objects.filter(address_id=address_id).count() == 1:
            Object.objects.get(slug=self.kwargs.get('slug')).delete()
        obj.delete()
        product = Product.objects.get(name=obj.name)
        Product.objects.filter(name=obj.name).update(quality=product.quality + obj.quality)
        return redirect('object_list')

    # def get_success_url(self):  # редирект на предыдущию страницу, через связный объект
    #     slug = Object.objects.get(pk=self.get_object().address.pk).slug
    #     return reverse('object_list', kwargs={'slug': slug})
