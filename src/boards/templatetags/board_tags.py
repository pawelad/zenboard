"""
board module template tags
"""
from django import template

from boards.issues import BoardIssue
from boards.models import Board


register = template.Library()


@register.simple_tag
def user_available_boards(user):
    """
    Get boards that are currently available to the user.

    :param user: Django user instance
    :type user: django.contrib.auth.models.User
    :returns: a list of available boards
    :rtype: list of boards.Board
    """
    if not user.is_authenticated:
        return []

    return Board.objects.for_user(user)


@register.simple_tag
def issue_details(board, issue_number):
    """
    Get issue details data.

    :param board: board instance
    :type board: boards.models.Board
    :param issue_number: issue number
    :type issue_number: int
    :returns: board issue details
    :rtype: dict
    """
    issue = BoardIssue(board, issue_number)
    return issue.details()
