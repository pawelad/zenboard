"""
board module template tags
"""
from django import template

from boards.models import Board


register = template.Library()


@register.simple_tag
def user_available_boards(user):
    """
    Helper method for determining that boards are currently available
    to the user.

    :param user: Django user instance
    :type user: django.contrib.auth.models.User
    :returns: a list of available boards
    :rtype: list of boards.Board
    """
    if not user.is_authenticated:
        return []

    return Board.objects.for_user(user)
