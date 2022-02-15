from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import start_page

urlpatterns = [
    path('', start_page),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
