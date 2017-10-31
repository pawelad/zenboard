"""
boards module API views
"""
from django.core.cache import cache
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from boards.issues import Issue
from boards.models import Board
from boards.serializers import BoardSerializer


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint returns boards available to currently logged in user.

    It's readonly and has four simple methods:

    - `/`: Returns a list of boards available to currently logged in user.
    - `/:pk/`: Returns specified board details.
    - `/:pk/pipelines/`: Returns board pipelines details.
    - `/:pk/issue/:issue_number/`: Returns board issue details.
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

    @detail_route(methods=['get'], suffix='pipelines')
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

    @detail_route(methods=['get'], suffix='issue details',
                  url_name='issue', url_path='issue/(?P<issue_number>\d+)')
    def issue(self, request, pk=None, issue_number=None):
        """
        Returns board pipelines data.

        Uses cache by default - to force refresh you can pass a
        `force_refresh` GET parameter.
        """
        board = self.get_object()
        gh_repo = board.get_github_repository_client
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

        issue = Issue(gh_repo.issue(issue_number))
        issue_details = cache.get_or_set(
            key=board.get_cache_key('issue:{}'.format(issue_number)),
            default=lambda: issue.get_details(board.filter_sign),
        )

        return Response(issue_details)
