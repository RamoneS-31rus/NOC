from django.urls import path
from .views import ProfileView, ProfileUpdate

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('<int:pk>/edit/', ProfileUpdate.as_view(), name='profile_update'),
]
