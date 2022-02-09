from django.urls import path
from.views import (
    HouseList, HouseUpdate, RequestList, RequestCreate, RequestUpdate, RequestStatus,
)


urlpatterns = [
    path('houses/', HouseList.as_view(), name='house_list'),
    path('houses/<int:pk>/edit/', HouseUpdate.as_view(), name='house_update'),
    path('request/<int:pk>/create/', RequestCreate.as_view(), name='request_create'),
    path('request/<int:pk>/edit/', RequestUpdate.as_view(), name='request_update'),
    path('requests/new/', RequestList.as_view(template_name='gpon/requests_new.html'), name='requests_new'),
    path('requests/in-progress/', RequestList.as_view(template_name='gpon/requests_in_progress.html'), name='requests_in_progress'),
    path('requests/completed/', RequestList.as_view(template_name='gpon/requests_completed.html'), name='requests_completed'),
    path('request/<int:pk>/finish/', RequestStatus.as_view(choice='finish'), name='request_finish'),
    path('request/<int:pk>/resume/', RequestStatus.as_view(choice='resume'), name='request_resume'),
    path('requests/statistic/', RequestList.as_view(template_name='gpon/requests_statistic.html'), name='requests_statistic'),
]
