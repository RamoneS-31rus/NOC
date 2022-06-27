from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db.models import Count

from .models import House, Request, Tariff
from storage.models import Product
from .forms import HouseForm, RequestFormCreate
from .filters import HouseFilter, RequestFilter


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
        if self.filterset_class == RequestFilter:
            queryset = self.model.objects.all()
            url = self.request.get_full_path()
            """
            Переопределяем queryset в зависимости от url запроса.
            """
            if 'inactive' in url:
                queryset = queryset.filter(status__isnull=True).order_by('-date_req')
            elif 'new' in url:
                queryset = queryset.filter(status='False', date_con__isnull=True).order_by('-date_req')
            elif 'in-progress' in url:
                queryset = queryset.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
            elif 'completed' in url:
                queryset = queryset.filter(status='True').order_by('-date_con')
            else:
                queryset = super().get_queryset()
        else:
            queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()
        # queryset = self.model.objects.all()
        # url = self.request.get_full_path()
        # filterset_class = self.filterset_class
        # if 'new' in url:  # queryset для 'new' формируется в RequestHiddenFilter
        #     filterset_class = RequestHiddenFilter
        # elif 'in-progress' in url:
        #     filterset_class = self.filterset_class
        #     queryset = queryset.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
        # elif 'completed' in url:
        #     filterset_class = self.filterset_class
        #     queryset = queryset.filter(status='True').order_by('-date_con')
        # else:
        #     queryset = super().get_queryset()
        # self.filterset = filterset_class(self.request.GET, queryset=queryset)
        # return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class HouseList(LoginRequiredMixin, FilteredListView):
    model = House
    template_name = 'gpon/house_list.html'
    filterset_class = HouseFilter
    paginate_by = 50


class HouseUpdate(LoginRequiredMixin, UpdateView):
    model = House
    form_class = HouseForm
    template_name = 'gpon/house_form.html'
    success_url = '/gpon/houses/'


class RequestList(LoginRequiredMixin, FilteredListView):
    model = Request
    # context_object_name = 'requests'
    filterset_class = RequestFilter
    paginate_by = 10

    # def get_queryset(self):
    #     qs = self.model.objects.all()
    #     url = self.request.get_full_path()
    #     if 'new' in url:
    #         qs = qs.filter(status='False', date_con__isnull=True).order_by('date_req')
    #     elif 'in-progress' in url:
    #         qs = qs.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
    #     elif 'completed' in url:
    #         qs = qs.filter(status='True').order_by('-date_con')
    #     return qs


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'gpon/request_detail.html'


class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    template_name = 'gpon/request_form_create.html'
    form_class = RequestFormCreate
    """Контекст для отображения адреса в форме создания заявки."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = House.objects.get(pk=self.kwargs.get('pk'))
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    """
    Заполняем поле user ('Принял заявку') на авторизованного пользователя.
    Заполняем поля стоимости тарифа и стоимости роутера в зависимости от выбранного тарифа.
    """
    def form_valid(self, form):
        obj = form.save(commit=False)
        # if self.request.user.groups.filter(name='Managers').exists():
        #     obj.manager = self.request.user
        # else:
        #     obj.manager = None
        obj.user = self.request.user

        obj.address = House.objects.get(pk=self.kwargs.get('pk'))

        if obj.tariff is not None:
            obj.tariff_cost = Tariff.objects.get(name=obj.tariff).price
        else:
            obj.tariff_cost = 0

        if obj.router is not None:
            obj.router_cost = Product.objects.get(name=obj.router).price
        else:
            obj.router_cost = 0

        obj.save()
        return redirect('requests_new')


class RequestUpdate(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Request
    form_class = None
    """Заполняем поле manager на авторизованного пользователя, если оно пустое и пользователь в группе Managers"""
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     if kwargs.get('instance').manager is None and self.request.user.groups.filter(name='Managers').exists():
    #         kwargs.get('instance').manager = self.request.user
    #     return kwargs
    """Заполняем поля стоимости тарифа и стоимости роутера в зависимости от выбранного."""
    def form_valid(self, form):
        obj = form.save(commit=False)
        if 'tariff' in form.changed_data:  # Проверяем менялось ли поле tariff
            if obj.tariff is not None:
                obj.tariff_cost = Tariff.objects.get(name=obj.tariff).price
            else:
                obj.tariff_cost = 0

        if 'router' in form.changed_data:  # Проверяем менялось ли поле router
            if obj.router is not None:
                obj.router_cost = Product.objects.get(name=obj.router).price
            else:
                obj.router_cost = 0
        """Заполняем поле "Менеджер" на авторизованного менеджера, если поле "Дата подключения" изменялось."""
        if 'date_con' in form.changed_data and obj.date_con is not None and self.request.user.groups.filter(name='Managers').exists():
            obj.manager = self.request.user
        elif 'note' in form.changed_data and obj.date_con is None and self.request.user.groups.filter(name='Managers').exists():
            obj.manager = self.request.user

        obj.save()
        return super().form_valid(form)


class RequestStatus(UpdateView):
    model = Request
    choice = None
    fields = []

    def post(self, request, *args, **kwargs):
        choice = self.choice
        obj = Request.objects.get(pk=self.kwargs.get('pk'))
        if choice == 'finish':
            if not obj.installer.all():
                messages.error(request, 'Заполните поле "Монтажники"')
            elif obj.tariff is None:
                messages.error(request, 'Заполните поле "Тариф"')
            elif obj.ont is None:
                messages.error(request, 'Заполните поле "Модель ONT"')
            elif obj.cord is None and obj.whose_cord is False:
                messages.error(request, 'Заполните поле "Оптический патч-корд"')
            elif obj.manager is None:
                messages.error(request, 'Поле "Менеджер" не заполнено')
            else:
                check_amount = obj.check_amount()
                if type(check_amount) == tuple and check_amount[0] == 'error':
                    messages.error(request, f'Недопустимая операция, в наличии не достаточно {check_amount[1]} для списания')
                else:
                    obj.status = True
                    obj.save()
                    House.objects.filter(pk=obj.address_id).update(status=House.completed)
                    obj.update_price()
                    obj.expense_product(request, check_amount)
        elif choice == 'resume':
            obj.status = False
            obj.save()
            House.objects.filter(pk=obj.address_id).update(status=House.ready)
            obj.income_product()
        elif choice == 'inactive':
            if not obj.note:
                messages.error(request, 'Заполните поле "Примечание"')
            else:
                obj.status = None
                obj.save()
        elif choice == 'active':
            obj.status = False
            obj.save()
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))


# class Statistic(LoginRequiredMixin, ListView):
#     model = Request
#     template_name = 'gpon/requests_statistics.html'
#     filterset_class = StatisticFilter
#
#     # def get_queryset(self):
#     #     qs = self.model.objects.all()
#     #     url = self.request.get_full_path()
#     #     if 'new' in url:
#     #         qs = qs.filter(status='False', date_con__isnull=True).order_by('date_req')
#     #     elif 'in-progress' in url:
#     #         qs = qs.filter(status='False').exclude(date_con__isnull=True).order_by('date_con')
#     #     elif 'completed' in url:
#     #         qs = qs.filter(status='True').order_by('-date_con')
#     #     return qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset = self.model.objects.all()
#         context['test'] = queryset.filter(status='True').aggregate(Count('address'))
#         context['req_inac'] = StatisticFilter(self.request.GET, queryset=queryset.filter(status=None))
#         context['req_new'] = StatisticFilter(self.request.GET, queryset=queryset.filter(status='False', date_con__isnull=True))
#         context['req_pro'] = StatisticFilter(self.request.GET, queryset=queryset.filter(status='False').exclude(date_con__isnull=True))
#         context['req_com'] = StatisticFilter(self.request.GET, queryset=queryset.filter(status='True'))
#         context['req_all'] = StatisticFilter(self.request.GET, queryset=queryset)
#         return context


def statistics(request):
    if request.user.is_authenticated:
        """Статус заявок"""
        req_inac = len(Request.objects.filter(status=None))
        req_new = len(Request.objects.filter(status='False', date_con__isnull=True))
        req_pro = len(Request.objects.filter(status='False').exclude(date_con__isnull=True))
        req_com = len(Request.objects.filter(status='True'))
        req_all = len(Request.objects.all())
        requests = {'req_inac': req_inac,
                    'req_new': req_new,
                    'req_pro': req_pro,
                    'req_com': req_com,
                    'req_all': req_all}
        """Статус домов"""
        cable = len(House.objects.filter(status='Нет кабеля'))
        welding = len(House.objects.filter(status='Необходима сварка'))
        ready = len(House.objects.filter(status='Готов к подключению'))
        completed = len(House.objects.filter(status='Подключен'))
        total = len(House.objects.all())
        # ready = 0  # Счетаем только дома по которым заявки не завершены
        # ready_list = House.objects.filter(status='Готов к подключению')
        # for house in ready_list:
        #     if not Request.objects.filter(address_id=house.id).exists() or not house.request.status:
        #         ready += 1
        houses = {'cable': cable,
                  'welding': welding,
                  'ready': ready,
                  'completed': completed,
                  'total': total}
        """Проданные роутеры"""
        router_list = Product.objects.filter(type__type_name="Роутеры")
        sold_routers = {'all': 0}
        for router in router_list:
            value = len(Request.objects.filter(status='True').exclude(router__isnull=True).filter(router__name=router))
            sold_routers.update({'all': int(sold_routers.get('all') + value)})
            sold_routers[str(router)] = value
        """Установленные ONT"""
        ont_list = Product.objects.filter(type__type_name="Оптические терминалы")
        sold_ont = {'all': 0}
        for ont in ont_list:
            value = len(Request.objects.filter(status='True').filter(ont__name=ont))
            sold_ont.update({'all': int(sold_ont.get('all') + value)})
            sold_ont[str(ont)] = value
        """Использованные патч-корды"""
        cord_list = Product.objects.filter(type__type_name="Оптические патч-корды")
        used_cord = {'all': 0}
        for cord in cord_list:
            value = len(Request.objects.filter(status='True').filter(cord__name=cord))
            used_cord.update({'all': int(used_cord.get('all') + value)})
            used_cord[str(cord)] = value
        """Стоимость всех подключений, тарифов и роутеров"""
        con_list = Request.objects.filter(status='True')
        cost = {'total': 0, 'connections': 0, 'tariffs': 0, 'routers': 0}
        for req in con_list:
            cost_con = req.cost_con
            tariff_cost = req.tariff_cost
            router_cost = req.router_cost
            # price_tariff = Tariff.objects.get(name=req.tariff).price
            # if req.router is None:
            #     price_router = 0
            # else:
            #     price_router = Product.objects.get(name=req.router).price
            cost.update({'total': int(cost.get('total') + cost_con)})
            cost.update({'connections': int(cost.get('connections') + (cost_con - router_cost - tariff_cost))})
            cost.update({'tariffs': int(cost.get('tariffs') + tariff_cost)})
            cost.update({'routers': int(cost.get('routers') + router_cost)})

        data = {'requests': requests,
                'houses': houses,
                "sold_routers": sold_routers,
                "sold_ont": sold_ont,
                "used_cord": used_cord,
                "cost": cost,
                }
        return render(request, 'gpon/statistics.html', context=data)
    else:
        return render(request, 'sign/login.html')
