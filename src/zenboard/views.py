"""
Zenboard application views
"""
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.contrib import messages

from boards.models import Board


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Zenboard home view
    """
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        """
        Extends Django's `get` method and redirect's the user to latest board.
        """
        boards = Board.objects.for_user(request.user)

        if boards:
            return redirect(boards.latest())
        else:
            if request.user.is_superuser:
                msg = (
                    "I'm sorry but there are no boards available. "
                    "You should probably <a href=\"{}\">create one</a>."
                ).format(reverse('admin:boards_board_add'))
            else:
                msg = (
                    "I'm sorry but there are no boards available. "
                    "You should ask the admin to create one "
                    "and share it with you."
                )

            messages.info(request, mark_safe(msg))

        return super().get(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    """
    Django login view
    """
    template_name = 'login.html'


class LogoutView(auth_views.LogoutView):
    """
    Django logout view
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Extends Django's `dispatch` method and adds a info message.
        """
        dispatch = super().dispatch(request, *args, **kwargs)
        messages.info(request, "You successfully logged out.")
        return dispatch
