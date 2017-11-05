"""
webhooks module URLs config
"""
from django.conf.urls import url

from webhooks import views


urlpatterns = [
    url(
        r'^github/$',
        views.GitHubWebhookReceiverView.as_view(),
        name='github',
    ),
    url(
        r'^zenhub/$',
        views.ZenHubWebhookReceiverView.as_view(),
        name='zenhub',
    ),
]
