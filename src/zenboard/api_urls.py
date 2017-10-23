"""
zenboard API URLs config
"""
from rest_framework import routers

from boards.api import BoardViewSet


router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet, 'board')

urlpatterns = router.urls
