from django.contrib.auth.models import User
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountForm
    template_name = 'profile/profile_update.html'
    queryset = User.objects.all()
    success_url = '/account'

