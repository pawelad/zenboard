"""
Test 'boards.apps' file
"""
from django.apps import AppConfig
from django.apps import apps as zenboard_apps


class TestBoardsConfig:
    """
    Test 'boards.apps.BoardsConfig'
    """
    def test_boards_app_config(self):
        """Test 'boards' module `AppConfig` instance"""
        boards_app_config = zenboard_apps.get_app_config('boards')

        assert isinstance(boards_app_config, AppConfig)
        assert boards_app_config.name == 'boards'
