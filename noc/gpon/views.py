from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render

from .models import House, Request
from .forms import HouseForm, RequestFormCreate, RequestFormUpdate
from .filters import HouseFilter


class HouseList(ListView):
    model = House
    template_name = 'gpon/house_list.html'
    context_object_name = 'house_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = HouseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class HouseCreate(CreateView):
    model = Request
    template_name = 'gpon/house_form.html'
    form_class = HouseForm
    success_url = '/gpon/houses/'

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user = self.request.user
    #     obj.save()
    #     return redirect('house_list')


class HouseUpdate(UpdateView):
    model = House
    form_class = HouseForm
    template_name = 'gpon/house_form.html'
    success_url = '/gpon/houses/'


class RequestList(ListView):
    model = Request
    context_object_name = 'requests'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = Request.objects.filter(status='False', date_con__isnull=True).order_by('-id')
        context['in_progress'] = Request.objects.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
        context['is_completed'] = Request.objects.filter(status='True').order_by('-id')
        context['total_houses'] = House.objects.all()
        context['cable_houses'] = House.objects.filter(status='Нет кабеля')
        context['welding_houses'] = House.objects.filter(status='Необходима сварка')
        context['ready_houses'] = House.objects.filter(status='Готов к подключению')
        context['sold_routers'] = Request.objects.filter(status='True').exclude(router__isnull=True)
        return context
    """
    Переопределяем queryset в зависимости от url запроса.
    """
    def get_queryset(self):
        qs = self.model.objects.all()
        url = self.request.get_full_path()
        if 'new' in url:
            qs = qs.filter(status='False', date_con__isnull=True).order_by('date_req')
        elif 'in-progress' in url:
            qs = qs.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
        elif 'completed' in url:
            qs = qs.filter(status='True').order_by('-date_con')
        return qs


class RequestCreate(CreateView):
    model = Request
    template_name = 'gpon/request_form_create.html'
    form_class = RequestFormCreate
    success_url = '/gpon/requests/new/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.address = House.objects.get(pk=self.kwargs.get('pk'))
        obj.save()
        return redirect('requests_new')


class RequestUpdate(UpdateView):
    model = Request
    template_name = 'gpon/request_form_update.html'
    form_class = RequestFormUpdate
    success_url = '/gpon/requests/in-progress/'


class RequestStatus(UpdateView):
    model = Request
    choice = None
    fields = []

    def post(self, request, *args, **kwargs):
        choice = self.choice
        obj = Request.objects.get(pk=self.kwargs.get('pk'))
        if choice == 'finish':
            obj.status = True
            obj.save()
        elif choice == 'resume':
            obj.status = False
            obj.save()
            return redirect('requests_in_progress')
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))

