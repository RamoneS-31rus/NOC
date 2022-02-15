from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render

from .models import House, Request
from .forms import HouseForm, RequestFormCreate, RequestFormUpdate
from .filters import HouseFilter


class RedirectToPreviousMixin:  # Миксин для редиректа на предыдущию страницу
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class HouseList(FilteredListView):
    model = House
    template_name = 'gpon/house_list.html'
    filterset_class = HouseFilter
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = HouseFilter(self.request.GET, queryset=self.get_queryset())
    #     return context


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
        context['total_requests'] = Request.objects.all()
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.groups.filter(name='Managers').exists():
            obj.manager = self.request.user
        else:
            obj.manager = None
        obj.address = House.objects.get(pk=self.kwargs.get('pk'))
        obj.save()
        return redirect('requests_new')


class RequestUpdate(RedirectToPreviousMixin, UpdateView):
    model = Request
    template_name = 'gpon/request_form_update.html'
    form_class = RequestFormUpdate

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if kwargs.get('instance').manager is None and self.request.user.groups.filter(name='Managers').exists():
            kwargs.get('instance').manager = self.request.user
        return kwargs


class RequestStatus(UpdateView):
    model = Request
    choice = None
    fields = []

    def post(self, request, *args, **kwargs):
        choice = self.choice
        obj = Request.objects.get(pk=self.kwargs.get('pk'))
        if choice == 'finish':
            obj.status = True
            obj.update_price()
            obj.save()
        elif choice == 'resume':
            obj.status = False
            obj.save()
            return redirect('requests_in_progress')
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))
