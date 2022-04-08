from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import AddressForm
from .models import Address
from gpon.models import District, House


class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'addressbook/form.html'
    form_class = AddressForm
    success_url = '/gpon/houses/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    """Переопределяем форму для создания объекта в моделе House после добавления адреса"""
    def form_valid(self, form):
        obj = form.save(commit=False)
        district_id = self.request.POST['district']  # достаём из формы id района
        obj.save()
        House.objects.create(address=Address.objects.get(id=Address.objects.order_by('id').last().id),
                             district=District.objects.get(id=district_id))
        return redirect('house_list')
