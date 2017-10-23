"""
zenboard utils
"""
from django.conf import settings
from github3 import GitHub

from zenhub_api import ZenHubAPI


class ValidateModelMixin:
    """
    DRF mixin that calls Django model validation
    """
    def validate(self, attrs):
        attrs = super().validate(attrs)
        obj = self.Meta.model(**attrs)
        obj.clean()
        return attrs


github_api = GitHub(
    token=settings.GITHUB_TOKEN,
)

zenhub_api = ZenHubAPI(
    token=settings.ZENHUB_API_TOKEN,
)
