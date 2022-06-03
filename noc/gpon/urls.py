from django.urls import path

from .forms import RequestFormUpdate, RequestInactiveFormUpdate
from.views import (
    HouseList, HouseUpdate, RequestDetailView, RequestList, RequestCreate, RequestUpdate, RequestStatus, statistics
)


urlpatterns = [
    path('houses/', HouseList.as_view(), name='house_list'),
    path('houses/<int:pk>/edit/', HouseUpdate.as_view(), name='house_update'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request_detail'),
    path('requests/inactive/', RequestList.as_view(template_name='gpon/requests_inactive.html'), name='requests_inactive'),
    path('requests/new/', RequestList.as_view(template_name='gpon/requests_new.html'), name='requests_new'),
    path('requests/in-progress/', RequestList.as_view(template_name='gpon/requests_in_progress.html'), name='requests_in_progress'),
    path('requests/completed/', RequestList.as_view(template_name='gpon/requests_completed.html'), name='requests_completed'),
    path('request/<int:pk>/create/', RequestCreate.as_view(), name='request_create'),
    path('request/<int:pk>/edit/', RequestUpdate.as_view(form_class=RequestFormUpdate,
                                                         template_name='gpon/request_form_update.html'), name='request_update'),
    path('request/<int:pk>/update/', RequestUpdate.as_view(form_class=RequestInactiveFormUpdate,
                                                           template_name='gpon/request_inactive_form_update.html'), name='request_inactive_update'),
    path('request/<int:pk>/inactive/', RequestStatus.as_view(choice='inactive'), name='request_inactive'),
    path('request/<int:pk>/active/', RequestStatus.as_view(choice='active'), name='request_active'),
    path('request/<int:pk>/finish/', RequestStatus.as_view(choice='finish'), name='request_finish'),
    path('request/<int:pk>/resume/', RequestStatus.as_view(choice='resume'), name='request_resume'),
    # path('requests/statistics/', Statistic.as_view(), name='requests_statistics'),
    path('statistics/', statistics, name='statistics')
]
