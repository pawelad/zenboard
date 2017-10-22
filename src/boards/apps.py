"""
boards module Django AppConfig integration
"""
from django.apps import AppConfig


class BoardsConfig(AppConfig):
    """
    Django app config for 'boards' module
    """
    name = 'boards'
    verbose_name = "Boards"
