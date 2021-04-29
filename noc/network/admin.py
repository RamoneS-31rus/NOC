from django.contrib import admin
from .models import Vlan, Switch, VlanHistory, SwitchHistory


admin.site.register(Vlan)
admin.site.register(Switch)
admin.site.register(VlanHistory)
admin.site.register(SwitchHistory)
