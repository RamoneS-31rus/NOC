from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
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
    # success_url = '/gpon/houses/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('house_list')


class HouseUpdate(UpdateView):
    model = House
    form_class = HouseForm
    template_name = 'gpon/house_form.html'
    success_url = '/gpon/houses/'


class RequestList(ListView):
    model = Request
    context_object_name = 'requests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_new'] = Request.objects.filter(status='False').filter(date_con__isnull=True).order_by('-id')
        context['in_progress'] = Request.objects.filter(status='False').exclude(date_con__isnull=True).order_by('-id')
        context['is_completed'] = Request.objects.filter(status='True').order_by('-id')
        context['sold_routers'] = Request.objects.filter(status='True').exclude(router__isnull=True)
        context['total_houses'] = House.objects.all()
        context['ready_houses'] = House.objects.filter(status='Готов к подключению')
        context['welding_houses'] = House.objects.filter(status='Необходима сварка')
        context['cable_houses'] = House.objects.filter(status='Нет кабеля')
        return context


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

