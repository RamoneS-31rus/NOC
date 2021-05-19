from django.urls import path
from.views import (
    AddressList, AddressDetail, AddressCreate, AddressUpdate, AddressDelete,
    ContactCreate, ContactUpdate, ContactDelete,
)


urlpatterns = [
    path('addresses/', AddressList.as_view(), name='address_list'),
    path('address/<slug:slug>', AddressDetail.as_view(), name='address_detail'),
    path('address/add/', AddressCreate.as_view(), name='address_add'),
    path('address/<slug:slug>/edit', AddressUpdate.as_view(), name='address_update'),
    path('address/<slug:slug>/delete/', AddressDelete.as_view(), name='address_delete'),
    path('address/<slug:slug>/contact/add/', ContactCreate.as_view(), name='contact_add'),
    path('address/<slug:slug>/contact/<int:pk>/edit/', ContactUpdate.as_view(), name='contact_update'),
    path('address/<slug:slug>/contact/<int:pk>/delete/', ContactDelete.as_view(), name='contact_delete'),
]
