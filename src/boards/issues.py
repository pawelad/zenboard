"""
boards module GitHub issue related code
"""
import re

import attr


UNFINISHED_TODO_ITEM = re.compile(r'^\s*- \[ \]', re.MULTILINE)
FINISHED_TODO_ITEM = re.compile(r'^\s*- \[x\]', re.MULTILINE)


@attr.s
class Issue:
    """
    Helper class for organizing GitHub issue related logic.
    """
    gh_issue = attr.ib()

    def _iter_comments(self):
        """Helper method for caching issue comments"""
        if not hasattr(self, 'comments'):
            self.comments = list(self.gh_issue.iter_comments())
        return self.comments

    def get_details(self, filter_sign=None):
        """
        Get GitHub issue details.

        :param filter_sign: filter sign
        :type filter_sign: str
        :returns: GitHub issue data
        :rtype: dict
        """
        return {
            'number': self.gh_issue.number,
            'title': self.gh_issue.title,
            'progress': self.get_progress(),
            'body': self.get_description(filter_sign),
            'comments': self.get_comments(filter_sign),
        }

    def get_description(self, filter_sign=None):
        """
        Get GitHub issue description.

        :param filter_sign: filter sign
        :type filter_sign: str
        :returns: GitHub issue description
        :rtype: dict
        """
        if filter_sign is None:
            body = self.gh_issue.body_html
        elif filter_sign is not None and filter_sign in self.gh_issue.body:
            body = self.gh_issue.body_html.replace(filter_sign, '')
        else:
            body = ''

        return body

    def get_comments(self, filter_sign=None):
        """
        Get GitHub issue comments.

        :param filter_sign: filter sign
        :type filter_sign: str
        :returns: GitHub issue comments data
        :rtype: dict
        """
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

    def get_progress(self, include_comments=True):
        """
        Return issue progress, which is the percentage of marked to do tasks.

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
