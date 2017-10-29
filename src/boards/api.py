"""
boards module API views
"""
from django.core.cache import cache
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from boards.models import Board
from boards.serializers import BoardSerializer
from boards.utils import get_issue_data


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
        qs = Board.objects.all()

        # Allow superuser to see all boards
        if not self.request.user.is_superuser:
            qs = qs.for_user(self.request.user)

        return qs

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

    @detail_route()
    def pipelines(self, request, pk=None):
        """
        Returns board pipelines data.

        Uses cache by default - to force refresh you can pass a
        `force_refresh` GET parameter.
        """
        board = self.get_object()

        # Check if user wants to force refresh
        if 'force_refresh' in self.request.GET:
            board.invalidate_cache('filtered_issues')
            board.invalidate_cache('pipelines')

        pipelines = cache.get_or_set(
            key=board.get_cache_key('pipelines'),
            default=lambda: board.get_pipelines(),
        )

        return Response(pipelines)

    @detail_route(url_name='issue', url_path='issue/(?P<issue_number>\d+)')
    def issue(self, request, pk=None, issue_number=None):
        """
        Returns board pipelines data.

        Uses cache by default - to force refresh you can pass a
        `force_refresh` GET parameter.
        """
        board = self.get_object()
        issue_number = int(issue_number)

        # Check if user wants to force refresh
        if 'force_refresh' in self.request.GET:
            board.invalidate_cache('filtered_issues')
            board.invalidate_cache('issue:{}'.format(issue_number))

        filtered_issues = cache.get_or_set(
            key=board.get_cache_key('filtered_issues'),
            default=lambda: board.get_filtered_issues(),
        )

        # User should only be able to access the issue data if he has access
        # to a board that this issue belongs to
        if issue_number not in filtered_issues:
            raise Http404

        issue_data = cache.get_or_set(
            key=board.get_cache_key('issue:{}'.format(issue_number)),
            default=lambda: get_issue_data(board, issue_number),
        )

        return Response(issue_data)
