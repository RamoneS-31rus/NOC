from django.urls import path
from.views import VlanList, VlanDetail, VlanUpdate, SwitchList, SwitchDetail, SwitchUpdate, SwitchCreate


urlpatterns = [
    path('vlans/', VlanList.as_view(), name='vlan_list'),
    path('vlan/<int:pk>', VlanDetail.as_view(), name='vlan_detail'),
    path('vlan/<int:pk>/edit/', VlanUpdate.as_view(), name='vlan_update'),
    path('search/', VlanList.as_view(template_name='search.html'), name='search'),
    path('switches/', SwitchList.as_view(), name='switch_list'),
    path('switch/<int:pk>', SwitchDetail.as_view(), name='switch_detail'),
    path('switch/<int:pk>/edit/', SwitchUpdate.as_view(), name='switch_update'),
    path('switch/add/', SwitchCreate.as_view(), name='switch_create'),
    #path('search/', PostSearch.as_view(), name='search'),
]
