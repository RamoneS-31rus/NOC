from django.urls import path

from .filters import RequestFilter, RequestHiddenFilter
from.views import (
    HouseList, HouseUpdate, RequestDetailView, RequestList, RequestCreate, RequestUpdate, RequestStatus, statistic
)


urlpatterns = [
    path('houses/', HouseList.as_view(), name='house_list'),
    path('houses/<int:pk>/edit/', HouseUpdate.as_view(), name='house_update'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request_detail'),
    path('requests/new/', RequestList.as_view(template_name='gpon/requests_new.html',
                                              filterset_class=RequestHiddenFilter), name='requests_new'),
    path('requests/in-progress/', RequestList.as_view(template_name='gpon/requests_in_progress.html',
                                                      filterset_class=RequestFilter), name='requests_in_progress'),
    path('requests/completed/', RequestList.as_view(template_name='gpon/requests_completed.html',
                                                    filterset_class=RequestFilter), name='requests_completed'),
    path('request/<int:pk>/create/', RequestCreate.as_view(), name='request_create'),
    path('request/<int:pk>/edit/', RequestUpdate.as_view(), name='request_update'),
    path('request/<int:pk>/finish/', RequestStatus.as_view(choice='finish'), name='request_finish'),
    path('request/<int:pk>/hide/', RequestStatus.as_view(choice='hide'), name='request_hide'),
    path('request/<int:pk>/resume/', RequestStatus.as_view(choice='resume'), name='request_resume'),
    # path('requests/statistic/', RequestList.as_view(template_name='gpon/statistic.html'), name='requests_statistic'),
    path('statistic/', statistic, name='statistic')
]
