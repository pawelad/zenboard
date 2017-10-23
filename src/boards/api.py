"""
boards module API views
"""
from rest_framework import viewsets

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
