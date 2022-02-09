from django.urls import path
from .views import AddressCreate


urlpatterns = [
    path('create/', AddressCreate.as_view(), name='address_create'),

]
