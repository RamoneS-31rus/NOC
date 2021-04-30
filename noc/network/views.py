from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Vlan, Switch, VlanHistory, SwitchHistory
from .forms import VlanForm, SwitchForm
from .filters import VlanFilter, SwitchFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django_filters.views import FilterView


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


class SwitchList(LoginRequiredMixin, ListView):
    model = Switch
    template_name = 'network/switch_list.html'
    context_object_name = 'switches'
    paginate_by = 100
    #form_class = VlanForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        context['filter'] = SwitchFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SwitchDetail(LoginRequiredMixin, DetailView):
    model = Switch
    template_name = 'network/switch_detail.html'
    context_object_name = 'switch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        if len(SwitchHistory.objects.filter(switch_order=self.kwargs.get('pk'))) > 1:
            context['history'] = SwitchHistory.objects.filter(switch_order=self.kwargs.get('pk'))[1::]
        else:
            context['history'] = None
        return context


class SwitchUpdate(LoginRequiredMixin, UpdateView):
    model = Switch
    form_class = SwitchForm
    template_name = 'network/switch_update.html'
    #permission_required = 'switch.change_switch'

    # def post(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     print(object)
    #     print(object.switch_address)
    #     print(object.switch_status)
    #     if object.switch_status:
    #         print("***"+str(object))
    #         object.switch_address = 'Склад'
    #         print("***" + str(object.switch_address))
    #         return redirect(object.get_absolute_url())
    #     else:
    #         return super(SwitchUpdate, self).post(request, *args, **kwargs)


class SwitchCreate(LoginRequiredMixin, CreateView):
    model = Switch
    template_name = 'network/switch_create.html'
    form_class = SwitchForm
    #permission_required = 'switch.add_switch'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.switch_user = self.request.user
        post.switch_order = len(Switch.objects.all()) + 1
        post.save()
        return redirect('/network/switches')
