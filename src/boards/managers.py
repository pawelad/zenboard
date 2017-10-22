"""
boards module managers
"""
from django.db import models


class BoardsQuerySet(models.QuerySet):
    """
    Custom `QuerySet` instance for 'boards.Board' model.
    """
    def for_user(self, user):
        """
        Helper method for returning only boards available to passed user.

        :param user: Django user instance
        :type user: django.contrib.auth.models.User
        :returns: filtered queryset
        :rtype: django.db.models.QuerySet
        """
        return self.filter(
            is_active=True,
            whitelisted_users=user,
        )
