"""
ZenHub API wrapper
"""
from collections import OrderedDict
from urllib.parse import urljoin

import requests


class ZenHubAPIError(Exception):
    """Base ZenHub API error"""
    pass


class ZenHubAPI(object):
    """
    Simple ZenHub public API wrapper.

    Only endpoints we currently use are implemented, but it's written with the
    possibility of extending that functionality and possibly releasing as open
    source in the future.

    Docs:
        https://github.com/ZenHubIO/API
    """
    api_url = 'https://api.zenhub.io/p1/'

    def __init__(self, token):
        """
        Initializes the instance with passed API token.

        :param token: ZenHub API token
        :type token: str
        """
        self._session = requests.Session()

        # See https://github.com/ZenHubIO/API#authentication
        self._session.headers.update({
            'X-Authentication-Token': token,
        })

    def _get_response(self, method, endpoint, params=None):
        """
        Helper method to handle HTTP requests and catch API errors.

        :param method: valid HTTP method
        :type method: str
        :param endpoint: API endpoint
        :type endpoint: str
        :param params: extra parameters passed with the request
        :type params: dict
        :returns: API response
        :rtype: Response
        """
        url = urljoin(self.api_url, endpoint)
        response = getattr(self._session, method)(url, params=params)

        if response.status_code != requests.codes.ok:
            raise ZenHubAPIError(
                "Something went wrong: {}".format(response.json())
            )

        return response

    def get_board(self, repository_id):
        """
        Returns the Board's pipelines, plus the issues contained within each
        pipeline. It returns each issues' issue number, its position in the
        board, an is epic flag(true/false), and its Time Estimate.

        Docs:
            https://github.com/ZenHubIO/API#get-the-zenhub-board-data-for-a-repository

        :param repository_id: GitHub repository ID
        :type repository_id: str
        :returns: ZenHub board pipelines
        :rtype: OrderedDict
        """
        endpoint = 'repositories/{}/board'.format(repository_id)
        response = self._get_response(method='get', endpoint=endpoint)
        data = response.json(object_pairs_hook=OrderedDict)

        return data['pipelines'] if 'pipelines' in data else data
