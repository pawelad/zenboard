"""
boards modile utils
"""


def get_issue_data(board, issue_number):
    """
    Get GitHub issue data.

    :param board: board instance
    :type  board: boards.models.Board
    :param issue_number: GitHub issue number
    :type issue_number: int
    :returns: GitHub issue data
    :rtype: dict
    """
    gh_issue = board.get_github_repository_client().issue(issue_number)

    # Filter both issue body and comments by the filter sign
    if board.filter_sign:
        if board.filter_sign in gh_issue.body:
            body = gh_issue.body_html.replace(board.filter_sign, '')
        else:
            body = ''

        comments = list()
        for comment in gh_issue.iter_comments():
            if board.filter_sign in comment.body:
                body = comment.body_html.replace(board.filter_sign, '')
                comments.append({
                    'id': comment.id,
                    'body': body,
                })
    # No filter sign, show everything
    else:
        body = gh_issue.body_html

        comments = list()
        for comment in gh_issue.iter_comments():
            comments.append({
                'id': comment.id,
                'body': comment.body_html,
            })

    return {
        'number': issue_number,
        'title': gh_issue.title,
        'body': body,
        'comments': comments,
    }
