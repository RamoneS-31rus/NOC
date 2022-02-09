from django.contrib import admin
from django.contrib.auth.models import User

from .models import House, Tariff, Request


class AdminRequest(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminRequest, self).get_form(request, obj, **kwargs)
        form.base_fields['installer'].queryset = User.objects.filter(groups__name='Installers').order_by('last_name')
        form.base_fields['manager'].queryset = User.objects.filter(groups__name='Managers').order_by('last_name')
        form.base_fields['installer'].label_from_instance = lambda inst: "{} {}".format(inst.last_name, inst.first_name)
        form.base_fields['manager'].label_from_instance = lambda inst: "{} {}".format(inst.last_name, inst.first_name)
        return form


# admin.site.register(Area)
admin.site.register(House)
admin.site.register(Tariff)
admin.site.register(Request, AdminRequest)
