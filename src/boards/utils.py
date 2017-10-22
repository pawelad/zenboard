"""
boards module utils
"""
from django.conf import settings
from github3 import GitHub

from boards.zenhub_api import ZenHubAPI


github_api = GitHub(
    token=settings.GITHUB_TOKEN,
)

zenhub_api = ZenHubAPI(
    token=settings.ZENHUB_API_TOKEN,
)
