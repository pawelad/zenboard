"""
boards module serializers
"""
from rest_framework import serializers

from boards import models
from zenboard.utils import ValidateModelMixin


class BoardSerializer(ValidateModelMixin, serializers.ModelSerializer):
    """
    DRF serializer for 'boards.Board' Django model.
    """
    class Meta:
        model = models.Board
        fields = '__all__'
