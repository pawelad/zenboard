"""
Test 'webhooks.apps' file
"""
from django.apps import AppConfig
from django.apps import apps as zenboard_apps


class TestWebhooksConfig:
    """
    Test 'webhooks.apps.WebhooksConfig'
    """
    def test_boards_app_config(self):
        """Test 'webhooks' module `AppConfig` instance"""
        webhooks_app_config = zenboard_apps.get_app_config('webhooks')

        assert isinstance(webhooks_app_config, AppConfig)
        assert webhooks_app_config.name == 'webhooks'
