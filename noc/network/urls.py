from django.urls import path
from.views import (VlanListView, VlanDetailView, VlanCreateView, VlanUpdateView, VlanDeleteView,
                   SwitchListView, SwitchDetailView, SwitchCreateView, SwitchUpdateView)


urlpatterns = [
    path('vlans', VlanListView.as_view(), name='vlan_list'),
    path('vlan/<int:pk>', VlanDetailView.as_view(), name='vlan_detail'),
    path('vlan/<int:pk>/add/', VlanCreateView.as_view(), name='vlan_create'),
    path('vlan/<int:number>/order/<int:pk>/edit/', VlanUpdateView.as_view(), name='vlan_update'),
    path('vlan/<int:pk>/delete/', VlanDeleteView.as_view(), name='vlan_delete'),
    path('switches', SwitchListView.as_view(), name='switch_list'),
    path('switch/<int:pk>', SwitchDetailView.as_view(), name='switch_detail'),
    path('switch/add/', SwitchCreateView.as_view(), name='switch_create'),
    path('switch/<int:pk>/edit/', SwitchUpdateView.as_view(), name='switch_update'),
]
