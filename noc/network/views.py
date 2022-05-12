from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django_filters.views import FilterView

from .models import VlanNumber, Vlan, Switch, VlanHistory, SwitchHistory
from .forms import VlanForm, SwitchForm
from .filters import VlanFilter, SwitchFilter


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


class VlanListView(LoginRequiredMixin, FilteredListView):
    model = VlanNumber
    template_name = 'network/vlan_list.html'
    filterset_class = VlanFilter
    paginate_by = 100


class VlanDetailView(LoginRequiredMixin, DetailView):
    model = VlanNumber
    template_name = 'network/vlan_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = Vlan.objects.filter(number=self.kwargs.get('pk'))
        # context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        context['history'] = VlanHistory.objects.filter(number=self.kwargs.get('pk'))
        # if len(VlanHistory.objects.filter(number=self.kwargs.get('pk'))) > 1:
        #     context['history'] = VlanHistory.objects.filter(number=self.kwargs.get('pk'))[1::]
        # else:
        #     context['history'] = None
        return context


class VlanCreateView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Vlan
    template_name = 'network/vlan_form.html'
    form_class = VlanForm
    #permission_required = 'switch.add_switch'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.number_id = self.kwargs.get('pk')
        obj.user = self.request.user
        obj.save()
        VlanHistory.objects.create(
            number=obj.number, client=obj.client, used_for=obj.used_for, point_a=obj.point_a, point_b=obj.point_b,
            order=obj.order, speed=obj.speed, note=obj.note, user=obj.user
        )
        return redirect('vlan_detail', self.kwargs.get('pk'))


class VlanUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Vlan
    form_class = VlanForm
    template_name = 'network/vlan_form.html'
    #permission_required = 'vlan.change_vlan'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if form.changed_data:
            VlanHistory.objects.create(
                number=obj.number, client=obj.client, used_for=obj.used_for, point_a=obj.point_a, point_b=obj.point_b,
                order=obj.order, speed=obj.speed, note=obj.note, user=obj.user, status=True
            )
        obj.save()
        return super().form_valid(form)


class VlanDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    model = Vlan

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        VlanHistory.objects.create(
            number=obj.number, client=obj.client, used_for=obj.used_for, point_a=obj.point_a, point_b=obj.point_b,
            order=obj.order, speed=obj.speed, note=obj.note, user=obj.user, status=False
        )
        obj.delete()
        return redirect('vlan_detail', obj)


class SwitchListView(LoginRequiredMixin, FilteredListView):
    model = Switch
    template_name = 'network/switch_list.html'
    filterset_class = SwitchFilter
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        return context


class SwitchDetailView(LoginRequiredMixin, DetailView):
    model = Switch
    template_name = 'network/switch_detail.html'
    context_object_name = 'switch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_Administrators'] = self.request.user.groups.filter(name='Administrators').exists()
        context['history'] = SwitchHistory.objects.filter(order=self.kwargs.get('pk'))
        # if len(SwitchHistory.objects.filter(order=self.kwargs.get('pk'))) > 1:
        #     context['history'] = SwitchHistory.objects.filter(order=self.kwargs.get('pk'))[1::]
        # else:
        #     context['history'] = None
        return context


class SwitchCreateView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Switch
    template_name = 'network/switch_form.html'
    form_class = SwitchForm
    #permission_required = 'switch.add_switch'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.order = len(Switch.objects.all()) + 1
        obj.save()
        SwitchHistory.objects.create(
            order=obj.order, address=obj.address, ip=obj.ip, mac=obj.mac, model=obj.model,
            firmware=obj.firmware, serial=obj.serial, note=obj.note, user=obj.user
        )
        return redirect('switch_list')


class SwitchUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Switch
    form_class = SwitchForm
    template_name = 'network/switch_form.html'
    #permission_required = 'switch.change_switch'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if form.changed_data:
            SwitchHistory.objects.create(
                order=obj.order, address=obj.address, ip=obj.ip, mac=obj.mac, model=obj.model,
                firmware=obj.firmware, serial=obj.serial, note=obj.note, user=obj.user, status=True
            )
        obj.save()
        return super().form_valid(form)
