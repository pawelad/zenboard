"""
boards module GitHub issue related code
"""
import re

from django.core.cache import cache

import attr

UNFINISHED_TODO_ITEM = re.compile(r'^\s*- \[ \]', re.MULTILINE)
FINISHED_TODO_ITEM = re.compile(r'^\s*- \[x\]', re.MULTILINE)


@attr.s
class BoardIssue:
    """
    Helper class for organizing GitHub issue related logic. It's board specific
    because it includes description and comments body filtering, which depend
    on `Board.filter_sign` field.
    """
    board = attr.ib()
    issue_number = attr.ib()

    def __attr_post_init__(self):
        self.gh_issue = self.board.gh_repo.issue(
            number=self.issue_number,
        )

    def _iter_comments(self):
        """
        Helper method for caching issue comments.
        """
        if not hasattr(self, 'comments'):
            self.comments = list(self.gh_issue.iter_comments())
        return self.comments

    def _get_details(self):
        """
        Get uncached GitHub issue details.

        :returns: GitHub issue data
        :rtype: dict
        """
        self.gh_issue = self.board.gh_repo.issue(
            number=self.issue_number,
        )

        # Base
        issue_details = {
            'number': self.gh_issue.number,
            'title': self.gh_issue.title,
            'author': self.gh_issue.user.name or self.gh_issue.user.login,
            'state': self.gh_issue.state,
            'created_at': self.gh_issue.created_at,
            'updated_at': self.gh_issue.updated_at,
            'closed_at': self.gh_issue.closed_at,
        }

        # Assignee
        if self.gh_issue.assignee:
            issue_details['assignee'] = (
                self.gh_issue.assignee.name or self.gh_issue.assignee.login
            )

        # Labels
        labels = [l.name for l in self.gh_issue.labels]
        issue_details['labels'] = ', '.join(labels)

        # Custom
        issue_details['body'] = self._get_description()
        issue_details['comments'] = self._get_comments()
        issue_details['progress'] = self._get_progress()

        return issue_details

    def _get_description(self):
        """
        Get uncached GitHub issue description.

        :returns: GitHub issue description
        :rtype: dict
        """
        filter_sign = self.board.filter_sign

        if filter_sign is None:
            body = self.gh_issue.body_html
        elif filter_sign is not None and filter_sign in self.gh_issue.body:
            body = self.gh_issue.body_html.replace(filter_sign, '')
        else:
            body = ''

        return body

    def _get_comments(self):
        """
        Get uncached GitHub issue comments.

        :returns: GitHub issue comments data
        :rtype: dict
        """
        filter_sign = self.board.filter_sign

        comments = list()
        for comment in self._iter_comments():
            if filter_sign is None:
                body = comment.body_html
            elif filter_sign is not None and filter_sign in comment.body:
                body = comment.body_html.replace(filter_sign, '')
            else:
                continue

            comments.append({
                'id': comment.id,
                'url': comment.html_url,
                'body': body,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at,
            })

        return comments

    def _get_progress(self, include_comments=True):
        """
        Return uncached issue progress, which is the percentage of done
        to do tasks.

        :param include_comments: whether to include comments
        :type include_comments: bool
        :returns: issue progress
        :rtype: float or None
        """
        body = self.gh_issue.body

        if include_comments:
            for comment in self._iter_comments():
                body += '\n'
                body += comment.body

        unfinished = len(UNFINISHED_TODO_ITEM.findall(body))
        finished = len(FINISHED_TODO_ITEM.findall(body))

        if finished or unfinished:
            return finished / (finished + unfinished)
        else:
            return None

    def details(self):
        """
        Get cached (if possible) GitHub issue details.

        :returns: GitHub issue data
        :rtype: dict
        """
        return cache.get_or_set(
            key=self.get_cache_key(),
            default=self._get_details,
        )

    def get_cache_key(self):
        """
        Helper method for generating a resource cache key.

        :returns: current issue data unique cache key
        :rtype: str
        """
        return self.board.get_cache_key(
            'issue:{number}'.format(number=self.issue_number),
        )

    def invalidate_cache(self):
        """
        Helper method for invalidating issue cache.
        """
        cache.delete(self.get_cache_key())
