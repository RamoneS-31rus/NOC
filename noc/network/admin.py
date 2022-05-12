from django.contrib import admin
from .models import VlanNumber, Vlan, Switch, VlanHistory, SwitchHistory


admin.site.register(VlanNumber)
admin.site.register(Vlan)
admin.site.register(Switch)
admin.site.register(VlanHistory)
admin.site.register(SwitchHistory)
