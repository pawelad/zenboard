"""
Zenboard application views
"""
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Zenboard home view
    """
    template_name = 'base.html'


class LoginView(auth_views.LoginView):
    """
    Django login view
    """
    template_name = 'login.html'


class LogoutView(auth_views.LogoutView):
    """
    Django logout view
    """
