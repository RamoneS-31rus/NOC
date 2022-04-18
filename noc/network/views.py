from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Vlan, Switch, VlanHistory, SwitchHistory
from .forms import VlanForm, SwitchForm
from .filters import VlanFilter, SwitchFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django_filters.views import FilterView


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


class VlanList(LoginRequiredMixin, ListView):
    model = Vlan  # queryset = Vlan.objects.all()
    template_name = 'network/vlan_list.html'
    context_object_name = 'vlans'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = VlanFilter(self.request.GET, queryset=self.get_queryset())
        return context


# class PaginatedFilterViews(View):
#     def get_context_data(self, **kwargs):
#         context = super(PaginatedFilterViews, self).get_context_data(**kwargs)
#         if self.request.GET:
#             querystring = self.request.GET.copy()
#             if self.request.GET.get('page'):
#                 del querystring['page']
#             context['querystring'] = querystring.urlencode()
#         return context
#
#
# class VlanList(PaginatedFilterViews, FilterView):
#     model = Vlan
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = VlanFilter(self.request.GET, queryset=self.get_queryset())
#         return context


class VlanDetail(LoginRequiredMixin, DetailView):
    model = Vlan
    template_name = 'network/vlan_detail.html'
    context_object_name = 'vlan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        if len(VlanHistory.objects.filter(vlan_name=self.kwargs.get('pk'))) > 1:
            context['history'] = VlanHistory.objects.filter(vlan_name=self.kwargs.get('pk'))[1::]
        else:
            context['history'] = None
        return context


class VlanUpdate(LoginRequiredMixin, UpdateView):
    model = Vlan
    form_class = VlanForm
    template_name = 'network/vlan_update.html'
    #permission_required = 'vlan.change_vlan'


class SwitchList(LoginRequiredMixin, FilteredListView):
    model = Switch
    template_name = 'network/switch_list.html'
    filterset_class = SwitchFilter
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        # context['filter'] = SwitchFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SwitchDetail(LoginRequiredMixin, DetailView):
    model = Switch
    template_name = 'network/switch_detail.html'
    context_object_name = 'switch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        if len(SwitchHistory.objects.filter(order=self.kwargs.get('pk'))) > 1:
            context['history'] = SwitchHistory.objects.filter(order=self.kwargs.get('pk'))[1::]
        else:
            context['history'] = None
        return context


class SwitchCreate(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Switch
    template_name = 'network/switch_form.html'
    form_class = SwitchForm
    #permission_required = 'switch.add_switch'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.order = len(Switch.objects.all()) + 1
        obj.save()
        return redirect('/network/switches')


class SwitchUpdate(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Switch
    form_class = SwitchForm
    template_name = 'network/switch_form.html'
    #permission_required = 'switch.change_switch'

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user = self.request.user
    #     if obj.status:
    #         obj.address = 'Склад'
    #     obj.save()
    #     return redirect('/network/switches')
