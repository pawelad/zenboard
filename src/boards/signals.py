"""
boards module signals
"""
import logging

from django.dispatch import receiver

from boards.issues import BoardIssue
from boards.models import Board
from webhooks.signals import github_event, zenhub_event


logger = logging.getLogger(__name__)


@receiver(github_event)
def invalidate_issue_details_cache(sender, event, guid, payload, **kwargs):
    """
    Invalidate GitHub issue details cache when it changes.
    """
    if event in ['issues', 'issue_comment']:
        issue_number = payload['issue']['number']
        repository = payload['repository']['full_name']
        boards = Board.objects.filter(github_repository=repository)

        for board in boards:
            board.invalidate_cache('filtered_issues')
            board.filtered_issues()

            board_issue = BoardIssue(board, issue_number)
            board_issue.invalidate_cache()
            board_issue.details()

            logger.info(
                "Updated issue {issue_number} for board {board!r} "
                "via webhook".format(
                    issue_number=issue_number,
                    board=board,
                )
            )


@receiver(zenhub_event)
def invalidate_board_pipeline_cache(sender, event, payload, **kwargs):
    """
    Invalidate ZenHub board pipelines data when it changes.
    """
    if event in ['issue_transfer', 'issue_reprioritized']:
        repository = '{}/{}'.format(
            payload['organization'], payload['repo'],
        )
        boards = Board.objects.filter(github_repository=repository)

        for board in boards:
            board.invalidate_cache('pipelines')
            board.pipelines()

            logger.info(
                "Updated pipelines for board {board!r} via webhook".format(
                    board=board,
                )
            )
