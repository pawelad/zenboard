"""
zenboard utils
"""
import logging

from django.conf import settings
from github3 import GitHub

from zenhub_api import ZenHubAPI


logger = logging.getLogger(__name__)


class ValidateModelMixin:
    """
    DRF mixin that calls Django model validation
    """
    def validate(self, attrs):
        attrs = super().validate(attrs)
        obj = self.Meta.model(**attrs)
        obj.clean()
        return attrs


if not settings.GITHUB_TOKEN:
    logging.warning("GitHub API token not found")

github_api = GitHub(
    token=settings.GITHUB_TOKEN,
)


if not settings.GITHUB_TOKEN:
    logging.warning("ZenHub API token not found")

zenhub_api = ZenHubAPI(
    token=settings.ZENHUB_API_TOKEN,
)
