"""
webhooks module Django AppConfig integration
"""
from django.apps import AppConfig


class WebhooksConfig(AppConfig):
    """
    Django app config for 'webhooks' module
    """
    name = 'webhooks'
    verbose_name = "Webhooks"
