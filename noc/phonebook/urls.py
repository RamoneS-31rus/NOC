from django.urls import path
from.views import AddressList, AddressDetail


urlpatterns = [
    path('objects', AddressList.as_view(), name='address_list'),
    path('object/<slug:slug>', AddressDetail.as_view(), name='address_detail'),
]
