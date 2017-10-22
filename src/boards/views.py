"""
boards module related views
"""
from django.http import Http404
from django.views.generic import DetailView

from boards import models


class BoardDetailView(DetailView):
    """
    Board instance detail view
    """
    model = models.Board
    slug_url_kwarg = 'name'
    slug_field = 'name'
    template_name = 'boards/details.html'
    context_object_name = 'board'

    def get_object(self, queryset=None):
        """
        Extends Django's `get_object` method and makes sure that the
        logged in user should be able to access the board.
        """
        obj = super().get_object(queryset)

        if not obj.is_whitelisted(self.request.user):
            raise Http404

        return obj

    def get_context_data(self, **kwargs):
        """
        Extends Django's `get_context_data` method and adds board data.
        """
        kwargs['board_data'] = self.object.get_board_data()
        return super().get_context_data(**kwargs)
