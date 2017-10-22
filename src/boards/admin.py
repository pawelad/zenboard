"""
boards module Django Admin integration
"""
from django.contrib import admin

from boards import models


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Django Admin integration for `boards.Board` model.
    """
    list_display = (
        'pk', 'name', 'github_repository', 'github_labels', 'get_users',
        'is_active', 'created', 'modified',
    )
    list_filter = (
        'whitelisted_users', 'is_active', 'github_repository',
        'created', 'modified',
    )
    search_fields = ('name', 'github_repository')

    def get_users(self, obj):
        """Helper method for getting a string of whitelisted users"""
        users = [str(u) for u in obj.whitelisted_users.all()]
        return ', '.join(users) or '-'
