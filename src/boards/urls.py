"""
boards module URLs config
"""
from django.conf.urls import url

from boards import views


urlpatterns = [
    url(r'^(?P<name>\w+)/$', views.BoardDetailView.as_view(), name='details'),
]
