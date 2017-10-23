"""
boards module API views
"""
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from boards.models import Board
from boards.serializers import BoardSerializer


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint returns boards available to currently logged in user.
    """
    serializer_class = BoardSerializer

    def get_queryset(self):
        """
        Filter the boards queryset and only return user available boards.

        :returns: filtered queryset
        :rtype: django.db.models.QuerySet
        """
        return Board.objects.for_user(self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of boards available to currently logged in user.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns specified board details.
        """
        return super().retrieve(request, *args, **kwargs)

    @detail_route(methods=['get'])
    def pipelines(self, request, pk=None):
        """
        Returns board pipelines data
        """
        board = self.get_object()

        # Check if user wants to force refresh
        if 'force_refresh' in self.request.GET:
            cache.delete(board.get_pipelines_cache_key())

        pipelines = cache.get_or_set(
            key=board.get_pipelines_cache_key(),
            default=board.get_pipelines(),
        )

        return Response(pipelines)
