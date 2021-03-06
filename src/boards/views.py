"""
boards module related views
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from boards import models


class BoardDetailView(LoginRequiredMixin, DetailView):
    """
    Board instance detail view
    """
    model = models.Board
    template_name = 'boards/details.html'
    context_object_name = 'board'

    def get_queryset(self):
        """
        Extends Django's `get_object` method and makes sure that the
        logged in user should be able to access the board.
        """
        qs = super().get_queryset()

        # Allow superuser to see all boards
        if not self.request.user.is_superuser:
            qs = qs.for_user(self.request.user)

        return qs

    def get_context_data(self, **kwargs):
        """
        Extends Django's `get_context_data` method and adds board data.
        """
        board = self.object

        # Check if user wants to force refresh
        if 'force_refresh' in self.request.GET:
            board.invalidate_cache()

        kwargs['pipelines'] = board.pipelines()

        return super().get_context_data(**kwargs)
